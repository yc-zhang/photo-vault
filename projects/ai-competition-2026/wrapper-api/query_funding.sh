#!/usr/bin/env bash
# L1 Wrapper API: query_funding
# Mock: 查询 OGM Funding 余额、流入、待花、Forecast
# Usage: query_funding.sh

set -euo pipefail

cat <<'JSON'
{
  "success": true,
  "funding": {
    "budget_id": "OGM-2026-Q3",
    "period": "2026-Q3",
    "total_budget": 500000.00,
    "currency": "CNY",
    "spent": 218400.00,
    "committed": 95000.00,
    "available": 186600.00,
    "forecast_spend": 120000.00,
    "breakdown": {
      "spare_parts": {"budget": 300000.00, "spent": 145000.00, "available": 155000.00},
      "maintenance": {"budget": 120000.00, "spent": 52000.00, "available": 68000.00},
      "professional_services": {"budget": 80000.00, "spent": 21400.00, "available": 58600.00}
    }
  }
}
JSON
