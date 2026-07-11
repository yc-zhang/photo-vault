---
name: l1-query-hotline-calls
description: "Query 2911 hotline call statistics: total/connected/missed calls, connection rate, hourly breakdown, top call reasons."
---

# L1: Query Hotline Calls

Atomic L1 skill — 查询 2911 热线电话接入统计数据。

## Wrapper API

```bash
bash projects/ai-competition-2026/wrapper-api/query_hotline_calls.sh [--date YYYY-MM-DD]
```

默认查询当天。指定 `--date` 可查历史日期。

## Data Schema

```json
{
  "success": true,
  "hotline": "2911",
  "date": "2026-07-12",
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
    { "hour": "08:00-09:00", "total": 3, "connected": 3, "missed": 0 }
  ],
  "topCallReasons": [
    { "reason": "网络无法连接", "count": 15, "pct": 0.319 }
  ]
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| `totalCalls` | int | 来电总数 |
| `connectedCalls` | int | 接通数 |
| `missedCalls` | int | 未接通数 |
| `connectionRate` | float | 接通率 (0-1) |
| `avgWaitTimeSeconds` | int | 平均等待时长（秒） |
| `avgCallDurationSeconds` | int | 平均通话时长（秒） |
| `peakHour` | string | 高峰时段 |
| `peakHourCalls` | int | 高峰时段来电数 |
| `hourlyBreakdown` | array | 按小时分段统计 |
| `topCallReasons` | array | 来电原因 TOP 排行 |

## L1-Level Filtering

| Filter | Description |
|--------|-------------|
| by date | 指定查询日期 |

过滤后输出精简视图给 L2 使用。
