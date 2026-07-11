---
name: l1-query-hotline-workorders
description: "Query 2911 hotline work orders: count by level (L1-L4), status breakdown, overdue items, and per-WO details."
---

# L1: Query Hotline Work Orders

Atomic L1 skill — 查询 2911 热线产生的工单详情。

## Wrapper API

```bash
bash projects/ai-competition-2026/wrapper-api/query_hotline_workorders.sh [--date YYYY-MM-DD] [--level L1|L2|L3|L4] [--status pending|in_progress|resolved|closed]
```

默认查询当天全部工单。可用 `--level` / `--status` 过滤。

## Data Schema

```json
{
  "success": true,
  "hotline": "2911",
  "date": "2026-07-12",
  "summary": {
    "totalWorkOrders": 23,
    "byLevel": {
      "L1": { "count": 3, "label": "紧急", "pct": 0.130 }
    },
    "byStatus": {
      "pending": { "count": 4, "label": "待处理" }
    },
    "overdueCount": 2,
    "avgResolutionTimeMinutes": 85
  },
  "workOrders": [
    {
      "woId": "WO-20260712-001",
      "level": "L1",
      "title": "...",
      "category": "网络设备故障",
      "source": "2911热线",
      "callerName": "李建国",
      "callerDept": "IDC 运维部",
      "callTime": "2026-07-12T08:23:15",
      "status": "in_progress",
      "assignedTo": "张羽辰",
      "assignedTeam": "网络运维组",
      "slaDeadline": "2026-07-12T08:53:15",
      "resolutionTimeMinutes": null,
      "isOverdue": false,
      "notes": "..."
    }
  ]
}
```

## Fields (per Work Order)

| Field | Type | Description |
|-------|------|-------------|
| `woId` | string | 工单编号 |
| `level` | L1-L4 | 工单级别 |
| `title` | string | 工单标题 |
| `category` | string | 工单分类 |
| `callerName` | string | 来电人 |
| `callerDept` | string | 来电部门 |
| `callTime` | ISO 8601 | 来电时间 |
| `status` | enum | pending / in_progress / resolved / closed |
| `assignedTo` | string | 处理人（未分配="未分配"） |
| `assignedTeam` | string | 处理团队 |
| `slaDeadline` | ISO 8601 | SLA 截止时间 |
| `resolutionTimeMinutes` | int/null | 解决耗时（分钟），未解决为 null |
| `isOverdue` | bool | 是否超时 |
| `notes` | string | 处理备注 |

## Status & Level Enums

**Status:**

| Value | Label |
|-------|-------|
| `pending` | 待处理 |
| `in_progress` | 处理中 |
| `resolved` | 已解决 |
| `closed` | 已关闭 |

**Level:**

| Value | Label | SLA |
|-------|-------|-----|
| `L1` | 紧急 | 30 min |
| `L2` | 高 | 2 hours |
| `L3` | 中 | 4 hours |
| `L4` | 低 | 24 hours |

## L1-Level Filtering

| Filter | Description |
|--------|-------------|
| by date | 指定查询日期 |
| by level | 只看某一级别工单 |
| by status | 只看某种状态工单 |

过滤后输出精简视图给 L2 使用。
