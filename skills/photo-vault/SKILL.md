---
name: photo-vault
description: "Upload photos from a local folder to cloud storage. Currently supports Tencent Cloud COS; more storage backends coming soon. Built-in diff: scan local dir vs bucket, upload new/changed files by size."
---

# Photo Vault

照片备份到腾讯云 COS。

## Prerequisites

- `tccli` credentials at `~/.tccli/default.credential`
- COS Python SDK: `pip3 install coscmd` (brings `cos-python-sdk-v5`)

## Script

```bash
python3 skills/photo-vault/scripts/vault.py <command> [options]
```

## Config (set once)

Sets of the shared config (`~/.photo-vault/config.json`), then forget about it.

```bash
# Set it up once
vault.py config set region       ap-shanghai
vault.py config set bucket       my-pic-storage-1319010017
vault.py config set local_root   ~/Desktop/photo_output
vault.py config set cloud_prefix photo_output

# Check current config
vault.py config get
```

After config is set, most commands accept a **subfolder** name only.

## Commands

| Command | What it does |
|---------|-------------|
| `config get [key]` | Show config (all or one key) |
| `config set <key> <value>` | Set a config value |
| `list-buckets` | List all COS buckets |
| `list-objects [subfolder]` | List objects, resolved from config + subfolder |
| `diff [subfolder]` | **Core.** Compare local dir vs bucket, show cost estimate |
| `sync [subfolder]` | Diff + ask + upload in one go |
| `upload <local_path> <object_key>` | Upload a single file |
| `download <object_key> <local_path>` | Download a single object |
| `head <object_key>` | Object metadata |

`--region` and `--bucket` can still be passed to override config values.

## Workflow

### The One Flow — config → diff → confirm → upload

1. **配置一次**
   ```
   vault.py config set region ap-shanghai
   vault.py config set bucket my-bucket-123456
   vault.py config set local_root ~/Desktop/photo_output
   vault.py config set cloud_prefix photo_output
   ```

2. **平时只用说「传 Kyushu Trip」**
   → Claw 自动组装：
   - 本地 → `~/Desktop/photo_output/260501 Kyushu Trip/`
   - 云端 → `photo_output/260501 Kyushu Trip/`
   - region + bucket → 从配置读

3. Claw 跑 diff 汇报摘要 + 费用 → 问你是否确认

4. 你确认后上传

## Cost Reference (Tencent Cloud COS Standard Storage)

| Item | Price (Chinese Mainland) |
|------|--------------------------|
| PUT/COPY/POST/LIST requests | ¥0.01 / 10,000 requests |
| Storage | ¥0.099 / GB / month |
| GET/HEAD requests | ¥0.01 / 10,000 requests |

At personal photo scale (~20K objects, a few GB), the monthly cost is **well under ¥1**.

## Examples

```bash
# List all buckets
vault.py list-buckets --region ap-guangzhou

# List objects under photo_output/
vault.py list-objects

# Check what needs uploading from Kyushu Trip
vault.py diff "260501 Kyushu Trip"

# Upload a specific file
vault.py upload ~/photo.jpg vacation/photo.jpg --bucket another-bucket
```

## Notes

- Diff compares by **file size** (fast, sufficient for photos)
- 20K objects → ~20 list requests → ~5 seconds
