#!/usr/bin/env bash
# L1 Wrapper API: query_inventory
# Mock: 查询备件库/现网库存
# Usage: query_inventory.sh [--location <spare_parts|field>] [--part <part_name>]

set -euo pipefail

LOCATION="spare_parts"
PART=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --location) LOCATION="$2"; shift 2 ;;
    --part) PART="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

# Mock data
if [[ "$LOCATION" == "spare_parts" ]]; then
  cat <<'JSON'
{
  "success": true,
  "location": "spare_parts",
  "items": [
    {"part": "WS-C2960X-24TS-L", "name": "Cisco 2960X 24口交换机", "stock": 5, "min_stock": 3, "status": "OK"},
    {"part": "WS-C3850-48P-S",  "name": "Cisco 3850 48口 PoE 交换机", "stock": 2, "min_stock": 5, "status": "LOW"},
    {"part": "SFP-10G-SR",       "name": "Cisco 10G SFP+ 光模块", "stock": 12, "min_stock": 10, "status": "OK"},
    {"part": "CAB-SPWR-30CM",    "name": "Cisco StackPower 线缆 30cm", "stock": 0, "min_stock": 2, "status": "OUT"},
    {"part": "PWR-C1-350WAC",    "name": "Cisco 350W AC 电源模块", "stock": 4, "min_stock": 3, "status": "OK"},
    {"part": "AP-3802I-E-K9",    "name": "Cisco Aironet 3802i AP", "stock": 8, "min_stock": 10, "status": "LOW"},
    {"part": "QSFP-40G-SR4",     "name": "Cisco 40G QSFP+ 光模块", "stock": 3, "min_stock": 4, "status": "LOW"},
    {"part": "N9K-C93180YC-FX",  "name": "Nexus 93180YC-FX 交换机", "stock": 1, "min_stock": 2, "status": "LOW"}
  ]
}
JSON
else
  cat <<'JSON'
{
  "success": true,
  "location": "field",
  "items": [
    {"part": "WS-C2960X-24TS-L", "name": "Cisco 2960X 24口交换机", "deployed": 48, "failed": 1},
    {"part": "WS-C3850-48P-S",  "name": "Cisco 3850 48口 PoE 交换机", "deployed": 32, "failed": 0},
    {"part": "SFP-10G-SR",       "name": "Cisco 10G SFP+ 光模块", "deployed": 240, "failed": 3},
    {"part": "AP-3802I-E-K9",    "name": "Cisco Aironet 3802i AP", "deployed": 156, "failed": 2},
    {"part": "QSFP-40G-SR4",     "name": "Cisco 40G QSFP+ 光模块", "deployed": 80, "failed": 1},
    {"part": "N9K-C93180YC-FX",  "name": "Nexus 93180YC-FX 交换机", "deployed": 12, "failed": 0}
  ]
}
JSON
fi
