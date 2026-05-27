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

_DEFAULT_REGION = "ap-shanghai"
_DEFAULT_BUCKET = "my-pic-storage-1319010017"


def _client(region=None):
    r = region or _DEFAULT_REGION
    config = CosConfig(Region=r, SecretId=_creds["secretId"], SecretKey=_creds["secretKey"])
    return CosS3Client(config)


def _pp(obj):
    print(json_lib.dumps(obj, indent=2, ensure_ascii=False, default=str))


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


def cmd_diff(bucket, local_dir, prefix, region):
    """Compare local directory against COS bucket, return list of files to sync."""
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

    result = {
        "LocalDir": local_dir,
        "Bucket": bucket,
        "Prefix": prefix or "",
        "RemoteCount": len(remote),
        "LocalCount": len(local_files),
        "ToUpload": to_upload,
        "AlreadySynced": already_synced,
        "MissingLocally": missing_locally,
    }
    _pp(result)


# ── CLI dispatch ─────────────────────────────────────────────────────

def main():
    import argparse

    parser = argparse.ArgumentParser(description="photo-vault — backup photos to cloud")
    parser.add_argument("--region", default=_DEFAULT_REGION, help=f"COS region (default: {_DEFAULT_REGION})")

    sub = parser.add_subparsers(dest="command", required=True)

    # list-buckets
    sub.add_parser("list-buckets", help="List all COS buckets")

    # list-objects
    p = sub.add_parser("list-objects", help="List objects in a bucket")
    p.add_argument("--bucket", default=_DEFAULT_BUCKET)
    p.add_argument("--prefix", default="")

    # upload
    p = sub.add_parser("upload", help="Upload a local file")
    p.add_argument("--bucket", default=_DEFAULT_BUCKET)
    p.add_argument("local_path")
    p.add_argument("object_key")

    # download
    p = sub.add_parser("download", help="Download a COS object")
    p.add_argument("--bucket", default=_DEFAULT_BUCKET)
    p.add_argument("object_key")
    p.add_argument("local_path")

    # head
    p = sub.add_parser("head", help="Get object metadata")
    p.add_argument("--bucket", default=_DEFAULT_BUCKET)
    p.add_argument("object_key")

    # diff
    p = sub.add_parser("diff", help="Compare local dir with bucket")
    p.add_argument("--bucket", default=_DEFAULT_BUCKET)
    p.add_argument("--prefix", default="")
    p.add_argument("local_dir")

    args = parser.parse_args()

    if args.command == "list-buckets":
        cmd_list_buckets(args.region)
    elif args.command == "list-objects":
        cmd_list_objects(args.bucket, args.prefix, args.region)
    elif args.command == "upload":
        cmd_upload(args.bucket, args.local_path, args.object_key, args.region)
    elif args.command == "download":
        cmd_download(args.bucket, args.object_key, args.local_path, args.region)
    elif args.command == "head":
        cmd_head(args.bucket, args.object_key, args.region)
    elif args.command == "diff":
        cmd_diff(args.bucket, args.local_dir, args.prefix, args.region)


if __name__ == "__main__":
    main()
