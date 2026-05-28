#!/usr/bin/env python3
"""photo-vault: local photo backup/sync CLI using Tencent Cloud COS."""

import json, logging, os, sys, json as json_lib
from pathlib import Path

logging.basicConfig(level=logging.WARNING)

# ── auth ─────────────────────────────────────────────────────────────
_cred_path = os.path.expanduser("~/.tccli/default.credential")
if not os.path.exists(_cred_path):
    print("❌ Tencent Cloud credentials not found at ~/.tccli/default.credential", file=sys.stderr)
    sys.exit(1)

with open(_cred_path) as f:
    _creds = json.load(f)

from qcloud_cos import CosConfig, CosS3Client


def _client(region):
    config = CosConfig(Region=region, SecretId=_creds["secretId"], SecretKey=_creds["secretKey"])
    return CosS3Client(config)


def _pp(obj):
    print(json_lib.dumps(obj, indent=2, ensure_ascii=False, default=str))


# ── config ───────────────────────────────────────────────────────────

_CONFIG_DIR = os.path.expanduser("~/.photo-vault")
_CONFIG_FILE = os.path.join(_CONFIG_DIR, "config.json")

_DEFAULT_CONFIG = {
    "region": "",
    "bucket": "",
    "local_root": "",
    "cloud_prefix": "",
}


def _load_config():
    if os.path.exists(_CONFIG_FILE):
        with open(_CONFIG_FILE) as f:
            return {**_DEFAULT_CONFIG, **json.load(f)}
    return dict(_DEFAULT_CONFIG)


def _save_config(cfg):
    os.makedirs(_CONFIG_DIR, exist_ok=True)
    with open(_CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def cmd_config_get(key=None):
    cfg = _load_config()
    if key:
        print(f"{key} = {cfg.get(key, '')}")
    else:
        for k, v in cfg.items():
            print(f"  {k} = {v}")


def cmd_config_set(key, value):
    cfg = _load_config()
    if key not in _DEFAULT_CONFIG:
        print(f"❌ Unknown config key: {key}. Valid: {', '.join(_DEFAULT_CONFIG.keys())}", file=sys.stderr)
        sys.exit(1)
    cfg[key] = value
    _save_config(cfg)
    print(f"✅ {key} = {value}")


def _resolve(subfolder=None):
    """Resolve effective region/bucket/local_dir/cloud_prefix from config + overrides.
    
    If subfolder given, builds local_dir and cloud_prefix from config roots + subfolder.
    """
    cfg = _load_config()
    region = cfg["region"]
    bucket = cfg["bucket"]
    local_root = cfg["local_root"]
    cloud_prefix = cfg["cloud_prefix"]

    local_dir = local_root
    prefix = cloud_prefix

    if subfolder:
        local_dir = os.path.join(local_root, subfolder) if local_root else subfolder
        prefix = f"{cloud_prefix.rstrip('/')}/{subfolder}" if cloud_prefix else subfolder

    return region, bucket, local_dir, prefix


# ── commands ─────────────────────────────────────────────────────────

def cmd_list_buckets(region):
    client = _client(region)
    resp = client.list_buckets()
    _pp(resp.get("Buckets", {}).get("Bucket", []))


def cmd_list_objects(bucket, prefix, region):
    client = _client(region)
    marker = None
    all_objs = []
    while True:
        kwargs = {"Bucket": bucket, "MaxKeys": 1000}
        if marker:
            kwargs["Marker"] = marker
        if prefix:
            kwargs["Prefix"] = prefix
        resp = client.list_objects(**kwargs)
        contents = resp.get("Contents", [])
        all_objs.extend(contents)
        if resp.get("IsTruncated") == "true" and resp.get("NextMarker"):
            marker = resp["NextMarker"]
        else:
            break
    print(json_lib.dumps({"Count": len(all_objs), "Contents": all_objs}, indent=2, ensure_ascii=False, default=str))


def cmd_upload(bucket, local_path, object_key, region):
    if not os.path.isfile(local_path):
        print(f"❌ File not found: {local_path}", file=sys.stderr)
        sys.exit(1)
    client = _client(region)
    resp = client.upload_file(Bucket=bucket, Key=object_key, LocalFilePath=local_path, EnableMD5=True)
    print(f"✅ Uploaded {local_path} → cos://{bucket}/{object_key}")
    _pp(resp)


def cmd_download(bucket, object_key, local_path, region):
    client = _client(region)
    os.makedirs(os.path.dirname(local_path) or ".", exist_ok=True)
    client.download_file(Bucket=bucket, Key=object_key, DestFilePath=local_path)
    print(f"✅ Downloaded cos://{bucket}/{object_key} → {local_path}")


def cmd_head(bucket, object_key, region):
    client = _client(region)
    resp = client.head_object(Bucket=bucket, Key=object_key)
    _pp(resp)


def cmd_sync(bucket, local_dir, prefix, region):
    """Diff then upload all new/changed files."""
    import sys as _sys
    _sys.stdout.reconfigure(line_buffering=True)  # force flush on newline

    client = _client(region)

    # scan remote
    print("🔍 Scanning remote...", flush=True)
    marker = None
    remote = {}
    while True:
        kwargs = {"Bucket": bucket, "MaxKeys": 1000}
        if marker:
            kwargs["Marker"] = marker
        if prefix:
            kwargs["Prefix"] = prefix
        resp = client.list_objects(**kwargs)
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            remote[key] = {"Size": int(obj["Size"]), "ETag": obj["ETag"]}
        if resp.get("IsTruncated") == "true" and resp.get("NextMarker"):
            marker = resp["NextMarker"]
        else:
            break
    print(f"  Remote: {len(remote)} objects", flush=True)

    # scan local
    print("🔍 Scanning local...", flush=True)
    local_root = Path(local_dir).resolve()
    to_upload = []
    for fpath in local_root.rglob("*"):
        if fpath.is_file():
            rel = str(fpath.relative_to(local_root))
            key = f"{prefix.rstrip('/')}/{rel}" if prefix else rel
            st = fpath.stat()
            if key not in remote or remote[key]["Size"] != st.st_size:
                to_upload.append({"Key": key, "LocalPath": str(fpath), "Size": st.st_size})

    total = len(to_upload)
    total_bytes = sum(i["Size"] for i in to_upload)
    total_mb = round(total_bytes / 1024 / 1024, 1)
    print(f"  Local: {total} files to upload ({total_mb} MB)", flush=True)
    print()
    print(f"🚀 Starting upload of {total} files...", flush=True)
    print()

    ok = 0
    fail = 0
    last_report = 0
    for i, item in enumerate(to_upload, 1):
        try:
            client.upload_file(
                Bucket=bucket,
                Key=item["Key"],
                LocalFilePath=item["LocalPath"],
                EnableMD5=True
            )
            ok += 1
        except Exception as e:
            fail += 1
            print(f"  ❌ {item['Key']}: {e}", flush=True)
        
        # progress report every 50 or final
        if ok - last_report >= 50 or i == total:
            print(f"  [{i}/{total}] ✅ {ok} uploaded, ❌ {fail} failed ({round(i/total*100)}%)", flush=True)
            last_report = ok

    print()
    print(f"🏁 Done! {ok} uploaded, {fail} failed", flush=True)
    if fail > 0:
        print(f"   Rerun sync to retry failed files", flush=True)


def cmd_diff(bucket, local_dir, prefix, region):
    """Compare local directory against COS bucket."""
    client = _client(region)

    # scan remote
    marker = None
    remote = {}
    while True:
        kwargs = {"Bucket": bucket, "MaxKeys": 1000}
        if marker:
            kwargs["Marker"] = marker
        if prefix:
            kwargs["Prefix"] = prefix
        resp = client.list_objects(**kwargs)
        for obj in resp.get("Contents", []):
            key = obj["Key"]
            remote[key] = {"Size": int(obj["Size"]), "ETag": obj["ETag"], "LastModified": obj["LastModified"]}
        if resp.get("IsTruncated") == "true" and resp.get("NextMarker"):
            marker = resp["NextMarker"]
        else:
            break

    # scan local
    local_root = Path(local_dir).resolve()
    local_files = {}
    for fpath in local_root.rglob("*"):
        if fpath.is_file():
            rel = str(fpath.relative_to(local_root))
            key = f"{prefix.rstrip('/')}/{rel}" if prefix else rel
            st = fpath.stat()
            local_files[key] = {"Path": str(fpath), "Size": st.st_size}

    # diff
    to_upload = []
    already_synced = 0
    for key, info in local_files.items():
        if key not in remote:
            to_upload.append({"Key": key, "LocalPath": info["Path"], "Reason": "new"})
        elif remote[key]["Size"] != info["Size"]:
            to_upload.append({"Key": key, "LocalPath": info["Path"], "Reason": "size_changed", "RemoteSize": remote[key]["Size"], "LocalSize": info["Size"]})
        else:
            already_synced += 1

    missing_locally = [k for k in remote if k not in local_files]

    # cost estimate
    total_bytes = sum(os.path.getsize(i["LocalPath"]) for i in to_upload)
    total_mb = round(total_bytes / 1024 / 1024, 1)
    put_count = len(to_upload)
    request_fee = round(put_count * 0.01 / 10000, 6)
    storage_fee_per_month = round(total_bytes / 1024 / 1024 / 1024 * 0.099, 4)

    result = {
        "LocalDir": local_dir,
        "Bucket": bucket,
        "Prefix": prefix or "",
        "RemoteCount": len(remote),
        "LocalCount": len(local_files),
        "ToUpload": to_upload,
        "AlreadySynced": already_synced,
        "MissingLocally": missing_locally,
        "CostEstimate": {
            "FilesToUpload": put_count,
            "TotalDataMB": total_mb,
            "PutRequests": put_count,
            "PutRequestFeeCNY": request_fee,
            "MonthlyStorageFeeCNY": storage_fee_per_month
        }
    }
    _pp(result)


# ── CLI dispatch ─────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="photo-vault — backup photos to cloud")
    parser.add_argument("--region", help="COS region (overrides config)")
    parser.add_argument("--bucket", help="Bucket name (overrides config)")

    sub = parser.add_subparsers(dest="command", required=True)

    # ── config ──
    p_cfg = sub.add_parser("config", help="Manage configuration")
    p_cfg.add_argument("action", choices=["get", "set"], help="get all / get key / set key value")
    p_cfg.add_argument("key", nargs="?", default=None, help="Config key")
    p_cfg.add_argument("value", nargs="?", default=None, help="Config value")

    # ── list-buckets ──
    sub.add_parser("list-buckets", help="List all COS buckets")

    # ── list-objects ──
    p = sub.add_parser("list-objects", help="List objects in a bucket")
    p.add_argument("subfolder", nargs="?", default=None, help="Subfolder under config roots")

    # ── diff ──
    p = sub.add_parser("diff", help="Compare local subfolder with bucket")
    p.add_argument("subfolder", nargs="?", default=None, help="Subfolder under config roots")

    # ── sync ──
    p = sub.add_parser("sync", help="Diff + confirm + upload in one go")
    p.add_argument("subfolder", nargs="?", default=None, help="Subfolder under config roots")

    # ── upload ──
    p = sub.add_parser("upload", help="Upload a single file")
    p.add_argument("local_path")
    p.add_argument("object_key")

    # ── download ──
    p = sub.add_parser("download", help="Download a COS object")
    p.add_argument("object_key")
    p.add_argument("local_path")

    # ── head ──
    p = sub.add_parser("head", help="Get object metadata")
    p.add_argument("object_key")

    args = parser.parse_args()

    # ── config commands ──
    if args.command == "config":
        if args.action == "get":
            cmd_config_get(args.key)
        elif args.action == "set":
            if not args.key or not args.value:
                print("❌ Usage: config set <key> <value>", file=sys.stderr)
                sys.exit(1)
            cmd_config_set(args.key, args.value)
        return

    # ── other commands — resolve config ──
    region, bucket, local_dir, prefix = _resolve(args.subfolder if hasattr(args, 'subfolder') else None)

    # CLI overrides
    if args.region:
        region = args.region
    if args.bucket:
        bucket = args.bucket

    if not region:
        print("❌ --region is required. Set it via `config set region <value>` or pass --region", file=sys.stderr)
        sys.exit(1)
    if args.command != "list-buckets" and not bucket:
        print("❌ --bucket is required. Set it via `config set bucket <value>` or pass --bucket", file=sys.stderr)
        sys.exit(1)

    if args.command == "list-buckets":
        cmd_list_buckets(region)
    elif args.command == "list-objects":
        cmd_list_objects(bucket, prefix, region)
    elif args.command == "diff":
        if not local_dir or not os.path.isdir(local_dir):
            print(f"❌ Local directory not found: {local_dir}", file=sys.stderr)
            print("   Set local_root via `config set local_root <path>` or provide a subfolder", file=sys.stderr)
            sys.exit(1)
        cmd_diff(bucket, local_dir, prefix, region)
    elif args.command == "sync":
        if not local_dir or not os.path.isdir(local_dir):
            print(f"❌ Local directory not found: {local_dir}", file=sys.stderr)
            sys.exit(1)
        cmd_sync(bucket, local_dir, prefix, region)
    elif args.command == "upload":
        cmd_upload(bucket, args.local_path, args.object_key, region)
    elif args.command == "download":
        cmd_download(bucket, args.object_key, args.local_path, region)
    elif args.command == "head":
        cmd_head(bucket, args.object_key, region)


if __name__ == "__main__":
    main()
