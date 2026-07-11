#!/usr/bin/env bash
# L1 Wrapper API: create_po
# Mock: 创建采购单
# Usage: create_po.sh --part <part_number> --qty <quantity> --budget <budget_id> [--urgent]

set -euo pipefail

PART=""
QTY=""
BUDGET_ID="OGM-2026-Q3"
URGENT="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --part) PART="$2"; shift 2 ;;
    --qty) QTY="$2"; shift 2 ;;
    --budget) BUDGET_ID="$2"; shift 2 ;;
    --urgent) URGENT="true"; shift ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$PART" || -z "$QTY" ]]; then
  echo '{"success": false, "error": "Missing required params: --part and --qty"}' 
  exit 1
fi

PO_ID="PO-$(date +%Y%m%d)-$(printf '%04d' $((RANDOM % 10000)))"

cat <<JSON
{
  "success": true,
  "po_id": "$PO_ID",
  "part": "$PART",
  "quantity": $QTY,
  "budget_id": "$BUDGET_ID",
  "urgent": $URGENT,
  "status": "submitted",
  "estimated_delivery": "$(date -v+14d +%Y-%m-%d)",
  "approver": "Siru",
  "created_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
JSON
