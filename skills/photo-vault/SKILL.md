---
name: photo-vault
description: "Upload photos from a local folder to cloud storage. Currently supports Tencent Cloud COS; more storage backends coming soon. Built-in diff: scan local dir vs bucket, upload new/changed files by size."
metadata:
  openclaw:
    requires:
      env:
        - PHOTO_VAULT_BUCKET  # optional, defaults to my-pic-storage-1319010017
---

# Photo Vault

照片备份到腾讯云 COS。核心流程：diff → upload。

## Prerequisites

- `tccli` credentials configured at `~/.tccli/default.credential`
- `cos-python-sdk-v5` installed (via `pip3 install coscmd` which brings it)

## Script

`scripts/vault.py` — all operations go through this CLI.

```bash
python3 skills/photo-vault/scripts/vault.py <command> [options]
```

## Commands

| Command | What it does |
|---------|-------------|
| `list-buckets` | List all COS buckets under the account |
| `list-objects --prefix x` | List objects, optional prefix filter. Handles pagination automatically |
| `upload <local_path> <object_key>` | Upload a single file |
| `download <object_key> <local_path>` | Download a single object |
| `head <object_key>` | Get object metadata (size, ETag, last-modified) |
| `diff <local_dir>` | **Core operation.** Compare local dir vs bucket. Returns: what's new, what changed, what's already synced, what's missing locally |

## Workflows

### Full sync a local photo dir

```bash
# 1. See what's different
python3 scripts/vault.py diff --prefix photo_output/260501\ Kyushu\ Trip ~/Desktop/photo_output/260501\ Kyushu\ Trip/

# 2. Upload new ones (parse diff output, upload each ToUpload entry)
```

### Quick check what's in the vault

```bash
python3 scripts/vault.py list-objects --prefix photo_output/
```

## Notes

- `--bucket` defaults to `my-pic-storage-1319010017`, override with `--bucket <name>`
- `--region` defaults to `ap-shanghai`
- Diff compares by **file size** (fast, good enough for photos). Full ETag/MD5 check is opt-in if needed.
- 20K objects → 20 list requests → ~5 seconds. No cache/db needed at this scale.
