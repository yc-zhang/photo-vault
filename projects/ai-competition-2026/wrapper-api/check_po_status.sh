#!/usr/bin/env bash
# L1 Wrapper API: check_po_status
# Mock: 查询采购单状态
# Usage: check_po_status.sh --po-id <PO_ID>

set -euo pipefail

PO_ID=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --po-id) PO_ID="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

if [[ -z "$PO_ID" ]]; then
  echo '{"success": false, "error": "Missing required param: --po-id"}' 
  exit 1
fi

# Mock states based on PO ID hash
HASH=$(echo "$PO_ID" | md5 2>/dev/null | cut -c1-1 || echo "a")
case "$HASH" in
  [0-3]) STATUS="pending_approval"; STATUS_CN="待审批" ;;
  [4-6]) STATUS="approved"; STATUS_CN="已审批" ;;
  [7-9]) STATUS="shipping"; STATUS_CN="发货中" ;;
  *)     STATUS="delivered"; STATUS_CN="已到货" ;;
esac

cat <<JSON
{
  "success": true,
  "po_id": "$PO_ID",
  "status": "$STATUS",
  "status_cn": "$STATUS_CN",
  "updated_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "history": [
    {"time": "$(date -v-2d -u +%Y-%m-%dT%H:%M:%SZ)", "action": "submitted", "by": "System"},
    {"time": "$(date -v-1d -u +%Y-%m-%dT%H:%M:%SZ)", "action": "pending_approval", "by": "Siru"}
  ]
}
JSON
