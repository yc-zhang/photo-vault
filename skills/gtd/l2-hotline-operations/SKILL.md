---
name: l2-hotline-operations
display_name: Hotline Operations
description: "2911 hotline daily operations: call statistics, work order tracking, SLA monitoring, and escalation management."
---

# Hotline Operations

Domain Skill (L2) — 2911 热线日常运营：来电统计 + 工单追踪 + SLA 监控 + 升级管理。

## 触发

- "2911热线怎么样？"、"今天热线什么情况？"
- "热线报告"、"统计热线电话"
- "热线工单情况"、"有多少工单"
- "热线 SLA 有没有超时的？"

## 设计原则

**数据收集 → 工单分析 → 升级追踪** 三段式：

```
┌─────────────────────────────────────────────────┐
│              Hotline Operations                  │
│                                                 │
│  Phase 1: 数据收集                               │
│  ├─ 来电统计 (skill: l1-query-hotline-calls)     │
│  └─ 工单查询 (skill: l1-query-hotline-workorders)│
│           │                                     │
│           ▼                                     │
│  Phase 2: 工单分析                               │
│  ├─ 按级别分布 (L1 ~ L4)                         │
│  ├─ 按状态分布 (待处理/处理中/已解决/已关闭)       │
│  ├─ 超时识别 (SLA overdue)                      │
│  └─ 热点分类 (top call reasons)                  │
│           │                                     │
│           ▼                                     │
│  Phase 3: 升级追踪                               │
│  ├─ 超时工单详情                                 │
│  ├─ 待处理工单分配检查                            │
│  ├─ 通知升级 (skill: lark-im / im_send)          │
│  └─ 创建督办任务 (skill: lark-task / task_create) │
└─────────────────────────────────────────────────┘
```

用户可以选择：
- 停在 Phase 1（只看概览数据）
- 推进到 Phase 2（深入分析工单分布）
- 推进到 Phase 3（对超时/阻塞工单做升级处理）

---

## Phase 1: 数据收集

### Step 1.1: 查询来电统计

```bash
bash projects/ai-competition-2026/wrapper-api/query_hotline_calls.sh
```

→ 获得 `summary`（totalCalls / connectedCalls / missedCalls / connectionRate）+ `hourlyBreakdown` + `topCallReasons`

### Step 1.2: 查询工单概况

```bash
bash projects/ai-competition-2026/wrapper-api/query_hotline_workorders.sh
```

→ 获得 `summary`（totalWorkOrders / byLevel / byStatus / overdueCount）+ 完整工单列表

### 输出：今日概览

向用户展示概览卡片：

```
📞 2911 热线 — 今日概览 ({date})

   来电总数:   {totalCalls} 通
   接通率:     {connectionRate}%
   平均等待:   {avgWaitTimeSeconds}s

📋 热线工单: {totalWorkOrders} 张
   🔴 L1 (紧急): {L1_count}  |  🟠 L2 (高): {L2_count}
   🟡 L3 (中):   {L3_count}  |  🟢 L4 (低): {L4_count}

📊 处理状态:
   待处理: {pending}  |  处理中: {in_progress}
   已解决: {resolved}  |  已关闭: {closed}

⚠️ 超时: {overdueCount} 张  |  待分配: {unassigned} 张
```

### 用户可选动作

- "看看详细工单" → 进入 Phase 2
- "超时的工单有哪些？" → 进入 Phase 3
- "看看来电原因分布" → 展示 topCallReasons
- 结束

---

## Phase 2: 工单分析

### Step 2.1: 按级别展开

展示各级别工单明细：

```
🔴 L1 紧急工单 ({L1_count} 张) — SLA: 30min
   WO-001  IDC-A区核心交换机down         处理中  张羽辰  🔴超时
   WO-002  总部大楼全楼层断网             处理中  陈工    🔴超时
   WO-003  DCI 专线中断                   待处理  未分配  🔴超时

🟠 L2 高优先级 ({L2_count} 张) — SLA: 2h
   WO-004  VPN 网关负载过高              处理中  周工
   WO-005  财务系统访问异常              已解决  吴工    45min
   ...

🟡 L3 中优先级 ({L3_count} 张) — SLA: 4h
   ...

🟢 L4 低优先级 ({L4_count} 张) — SLA: 24h
   ...
```

### Step 2.2: 按状态分析

```
📊 状态分布:

   待处理 ({pending} 张):    需关注未分配项
   处理中 ({in_progress} 张): 正常推进
   已解决 ({resolved} 张):   平均耗时 {avgTime}min
   已关闭 ({closed} 张):     已完成归档
```

### Step 2.3: 来电原因热点

展示 `topCallReasons`，识别高频问题类型：

```
🔥 来电原因 TOP 5:
   1. 网络无法连接    — 15 次 (31.9%)
   2. VPN 无法登录    — 9 次  (19.1%)
   3. WiFi 信号弱     — 7 次  (14.9%)
   4. 打印机故障      — 5 次  (10.6%)
   5. 邮件无法收发    — 4 次  (8.5%)
```

### 用户可选动作

- "超时工单怎么处理？" → 进入 Phase 3
- "XX 工单详情" → 展示单张工单完整信息
- "按部门看工单" → 按 `callerDept` 分组
- 结束

---

## Phase 3: 升级追踪

当存在超时工单或待分配工单时触发。

### Step 3.1: 识别需升级项

从 `workOrders` 中筛选：

| 条件 | 严重度 | 原因 |
|------|--------|------|
| `status=pending AND isOverdue=true` | 🔴 严重 | 超时且无人处理 |
| `status=pending AND assignedTo=未分配` | 🔴 严重 | 工单未分配 |
| `status=in_progress AND isOverdue=true` | 🟠 高 | 处理中超时 |
| `status=pending AND assignedTo≠未分配` | 🟡 关注 | 已分配但未开始 |

### Step 3.2: 升级通知

对 🔴 严重项，使用 `lark-im` / `im_send` 通知对应团队负责人：

```
🚨 热线工单升级通知

以下工单需要立即关注：

🔴 WO-003  DCI 专线中断  待处理  未分配  ⏰超时15min
   → 请网络运维组尽快指派处理人

🔴 WO-002  总部大楼断网  处理中  陈工    ⏰超时10min  
   → 当前处理人: 陈工，请确认进展

提醒: 今天 2911 热线共 {overdueCount} 张工单超时
```

### Step 3.3: 创建督办任务

对超时工单创建跟踪任务，使用 `lark-task` / `task_create`：

```
任务标题: 热线工单 SLA 跟踪 — {date}
负责人: 张羽辰
截止日期: 当天 18:00

任务描述:
  2911 热线 {date} 工单 SLA 状态
  
  超时工单:
  | WO ID | 级别 | 标题 | 状态 | 处理人 | 超时 |
  |-------|------|------|------|--------|------|
  | WO-002 | L1 | 总部大楼断网 | in_progress | 陈工 | 10min |
  | WO-003 | L1 | DCI 专线中断 | pending | 未分配 | 15min |
  
  待分配工单: {unassignedCount} 张
  
  跟踪项:
  ☐ 超时工单确认处理进展
  ☐ 未分配工单指派处理人
  ☐ 当日工单清零检查
```

### 用户可选动作

- "催办 XX" → 调用 `lark-approval / approval_tasks_remind` 或 `lark-im / im_send`
- "查看历史趋势" → 调用 `l1-query-hotline-calls --date` 查过去几天
- 结束

---

## L1 Skill 调用清单

| Phase | Step | L1 Skill | 类型 |
|-------|------|---------|------|
| P1 | 来电统计 | `l1-query-hotline-calls` | Wrapper |
| P1 | 工单查询 | `l1-query-hotline-workorders` | Wrapper |
| P2 | 级别过滤 | `l1-query-hotline-workorders --level` | Wrapper |
| P2 | 状态过滤 | `l1-query-hotline-workorders --status` | Wrapper |
| P3 | 升级通知 | `im_send` | ✅ 飞书 lark-im |
| P3 | 督办任务 | `task_create` | ✅ 飞书 lark-task |
| P3 | 催办 | `im_send` | ✅ 飞书 lark-im |
