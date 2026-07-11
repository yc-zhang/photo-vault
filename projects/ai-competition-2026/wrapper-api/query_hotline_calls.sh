#!/usr/bin/env bash
# L1 Wrapper API: query_hotline_calls
# Mock: 查询 2911 热线电话接入统计数据
# Usage: query_hotline_calls.sh [--date YYYY-MM-DD]

set -euo pipefail

DATE="${1:-$(date +%Y-%m-%d)}"
if [[ "$DATE" == "--date" ]]; then
  DATE="$2"
fi

cat <<JSON
{
  "success": true,
  "hotline": "2911",
  "date": "$DATE",
  "summary": {
    "totalCalls": 47,
    "connectedCalls": 41,
    "missedCalls": 6,
    "connectionRate": 0.872,
    "avgWaitTimeSeconds": 18,
    "avgCallDurationSeconds": 245,
    "peakHour": "10:00-11:00",
    "peakHourCalls": 12
  },
  "hourlyBreakdown": [
    { "hour": "08:00-09:00", "total": 3, "connected": 3, "missed": 0 },
    { "hour": "09:00-10:00", "total": 8, "connected": 7, "missed": 1 },
    { "hour": "10:00-11:00", "total": 12, "connected": 10, "missed": 2 },
    { "hour": "11:00-12:00", "total": 6, "connected": 5, "missed": 1 },
    { "hour": "12:00-13:00", "total": 2, "connected": 2, "missed": 0 },
    { "hour": "13:00-14:00", "total": 5, "connected": 5, "missed": 0 },
    { "hour": "14:00-15:00", "total": 7, "connected": 6, "missed": 1 },
    { "hour": "15:00-16:00", "total": 4, "connected": 3, "missed": 1 }
  ],
  "topCallReasons": [
    { "reason": "网络无法连接", "count": 15, "pct": 0.319 },
    { "reason": "VPN 无法登录", "count": 9, "pct": 0.191 },
    { "reason": "WiFi 信号弱/断连", "count": 7, "pct": 0.149 },
    { "reason": "打印机故障", "count": 5, "pct": 0.106 },
    { "reason": "邮件无法收发", "count": 4, "pct": 0.085 },
    { "reason": "账号/密码问题", "count": 4, "pct": 0.085 },
    { "reason": "其他", "count": 3, "pct": 0.064 }
  ]
}
JSON
