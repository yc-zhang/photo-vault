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

All commands require `--region`. Commands that operate on a bucket require `--bucket`.

## Commands

| Command | What it does |
|---------|-------------|
| `list-buckets` | List all COS buckets |
| `list-objects` | List objects in a bucket, optional prefix, auto pagination |
| `upload <local_path> <object_key>` | Upload a single file |
| `download <object_key> <local_path>` | Download a single object |
| `head <object_key>` | Object metadata (size, ETag, last-modified) |
| `diff <local_dir>` | **Core.** Compare local dir vs bucket. Returns: new/changed/synced/missing + cost estimate |

## Workflow

### The One Flow — diff → confirm → upload

1. 你处理完照片放入一个文件夹（如 `photo_output/260601 Hokkaido Trip/`）

2. Claw 运行 diff：
   ```bash
   python3 scripts/vault.py diff \
     --region ap-guangzhou \
     --bucket my-bucket-123456 \
     --prefix photo_output/260601\ Hokkaido\ Trip \
     ~/Desktop/photo_output/260601\ Hokkaido\ Trip/
   ```

3. Claw 汇报摘要：
   - 新增 **N** 张待上传
   - 数据量 **X MB**
   - PUT 请求 **N** 次（每次 1 个对象）
   - 请求费用 ¥**0.0000X**（≈免费）
   - 月存储费用 ¥**X**（Standard 存储 ¥0.099/GB/月）
   - **询问用户：是否开始上传？**

4. 你确认后，Claw 逐张上传

5. 上传完毕，汇报结果

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
python3 scripts/vault.py list-buckets --region ap-guangzhou

# List objects under a prefix
python3 scripts/vault.py list-objects --region ap-shanghai --bucket my-bucket-123456 --prefix photo_output/

# Check what needs uploading from a folder
python3 scripts/vault.py diff \
  --region ap-shanghai \
  --bucket my-bucket-123456 \
  --prefix photo_output/260501\ Kyushu\ Trip \
  ~/Desktop/photo_output/260501\ Kyushu\ Trip/

# Upload a single file
python3 scripts/vault.py upload \
  --region ap-shanghai \
  --bucket my-bucket-123456 \
  ~/photo.jpg vacation/photo.jpg
```

## Notes

- Diff compares by **file size** (fast, sufficient for photos)
- 20K objects → ~20 list requests → ~5 seconds
