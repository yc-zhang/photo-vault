---
name: spare_parts_management
display_name: Spare Parts Management
description: "Manage spare parts inventory and status, generate replenishment plans based on actual inventory levels. When stock falls below minimum, query OGM funding and initiate procurement."
metadata:
  requires:
    scripts:
      - projects/ai-competition-2026/wrapper-api/query_inventory.sh
      - projects/ai-competition-2026/wrapper-api/query_funding.sh
      - projects/ai-competition-2026/wrapper-api/create_po.sh
      - projects/ai-competition-2026/wrapper-api/check_po_status.sh
---

# Spare Parts Management

Domain Skill (L2) — 备件库存管理 + 补货计划 + 采购触发。

## 触发

- "备件库存怎么样？"、"看看备件情况"
- "哪些备件需要补货？"、"生成补货计划"
- "采购 X 备件"、"库存不够了"
- "帮我处理备件采购"

## 设计原则

**库存感知 → 补货决策 → 采购执行** 三段式：

```
┌─────────────────────────────────────────────────┐
│                Spare Parts Management            │
│                                                 │
│  Phase 1: 库存感知                               │
│  ├─ 备件库库存 (spare_parts)                     │
│  └─ 现网库存 (field)                             │
│           │                                     │
│           ▼                                     │
│  Phase 2: 补货决策                               │
│  ├─ 库存状态分析 (OK / LOW / OUT)                │
│  ├─ 缺口计算 (min_stock - stock + field_failed)  │
│  └─ 生成补货计划                                 │
│           │                                     │
│           ▼                                     │
│  Phase 3: 采购执行（仅在需要时触发）              │
│  ├─ OGM Funding 余额查询                         │
│  ├─ 预算判断                                    │
│  ├─ 生成采购单                                   │
│  ├─ 通知采购同事                                 │
│  └─ 创建跟进任务                                 │
└─────────────────────────────────────────────────┘
```

用户可以选择停在 Phase 2（只看补货计划），也可以直接推进到 Phase 3（执行采购）。

---

## Phase 1: 库存感知

### Step 1.1: 查备件库库存

```bash
bash projects/ai-competition-2026/wrapper-api/query_inventory.sh --location spare_parts
```

提取所有备件的 `part`、`name`、`stock`、`min_stock`、`status`。

### Step 1.2: 查现网库存

```bash
bash projects/ai-competition-2026/wrapper-api/query_inventory.sh --location field
```

提取所有备件的 `deployed`、`failed`，了解现网故障对备件消耗的压力。

---

## Phase 2: 补货决策

### Step 2.1: 库存状态分析

按状态分类：

| 状态 | 条件 | 含义 |
|------|------|------|
| 🟢 OK | stock ≥ min_stock | 库存充足 |
| 🟡 LOW | 0 < stock < min_stock | 库存偏低，建议补货 |
| 🔴 OUT | stock = 0 | 库存耗尽，紧急补货 |

### Step 2.2: 缺口计算

```
建议补货数量 = max(min_stock - stock + field_failed, 1)
```

- `field_failed`：现网故障数，这些备件需要立即替换，消耗库存
- 最终补货数量确保库存回到 min_stock 以上，并覆盖即将发生的替换需求

### Step 2.3: 生成补货计划

输出补货计划表格：

```
📊 备件补货计划

| 备件 | 型号 | 库存 | 最低 | 现网故障 | 建议补货 | 紧急度 |
|------|------|------|------|---------|---------|--------|
| Cisco 3850 | WS-C3850-48P-S | 2 | 5 | 0 | 3 | 🟡 LOW |
| StackPower线缆 | CAB-SPWR-30CM | 0 | 2 | 0 | 2 | 🔴 OUT |
| Aironet AP | AP-3802I-E-K9 | 8 | 10 | 2 | 4 | 🟡 LOW |
```

### Step 2.4: 询问用户

如果存在 LOW/OUT 项，询问：

> 以下备件需要补货，是否启动采购流程？
> - WS-C3850-48P-S ×3
> - CAB-SPWR-30CM ×2
> - AP-3802I-E-K9 ×4
>
> 回复「采购」或指定具体备件来启动。

---

## Phase 3: 采购执行

仅在 Phase 2 确认后、或用户直接指定采购时触发。

### Step 3.1: 解析采购意图

从用户消息或 Phase 2 补货计划中提取：
- **备件型号**：如 "WS-C3850-48P-S"
- **数量**：Phase 2 计算的建议补货数量，或用户显式指定
- **是否紧急**：OUT 状态自动标记为紧急

### Step 3.2: 查 OGM Funding 余额

```bash
bash projects/ai-competition-2026/wrapper-api/query_funding.sh
```

检查 `funding.breakdown.spare_parts.available` 是否足够。

**单价估算（mock）：**

| 备件类型 | 单价 (CNY) |
|---------|-----------|
| 交换机 (2960/3850/Nexus) | 15,000 – 80,000 |
| 光模块 (SFP/QSFP) | 500 – 3,000 |
| AP | 3,000 |
| 电源/线缆 | 500 – 2,000 |

预估总价 = 数量 × 单价，与 `spare_parts.available` 对比。

**预算不足处理：**
- 告知用户缺口金额
- 选项：① 降低数量 ② 走特殊审批 ③ 取消

### Step 3.3: 生成采购单

```bash
bash projects/ai-competition-2026/wrapper-api/create_po.sh \
  --part "<PART_NUMBER>" \
  --qty <QUANTITY> \
  --budget "OGM-2026-Q3"
```

紧急采购加 `--urgent`。记录返回的 `po_id`。

### Step 3.4: 通知采购同事 (Siru)

使用飞书 `im_send`：

```
📦 新采购单 — {po_id}

备件：{part_name} ({part_number})
数量：{qty} 台
预估：¥{estimated_cost}
到货：{estimated_delivery}
紧急：{urgent}

请在飞书审批处理 🙏
```

### Step 3.5: 创建跟进任务

使用飞书 `task_create`：

```
标题：跟进采购 {po_id} — {part_name}
负责人：当前用户
截止：{estimated_delivery}
描述：OGM 备件采购跟踪，单号 {po_id}
```

### Step 3.6: 汇总报告

```
✅ 采购已发起

采购单号   PO-20260711-0877
备件       Cisco 3850 48口 PoE (WS-C3850-48P-S)
数量       3 台（补至最低库存 5）
预算       spare_parts ¥155,000 → 预估 ¥45,000 ✅
审批       Siru
到货       2026-07-25
任务       跟进任务已创建 ✅
通知       已通知 Siru ✅
```

---

## L1 Skill 调用清单

| Phase | Step | L1 Skill | 类型 |
|-------|------|---------|------|
| P1 | 查备件库 | `query_inventory --location spare_parts` | Wrapper |
| P1 | 查现网 | `query_inventory --location field` | Wrapper |
| P2 | 缺口计算 | 业务逻辑（L2 层） | — |
| P3 | 查 Funding | `query_funding` | Wrapper |
| P3 | 生成采购单 | `create_po` | Wrapper |
| P3 | 通知同事 | `im_send` | ✅ 飞书 lark-im |
| P3 | 创建任务 | `task_create` | ✅ 飞书 lark-task |
| P3 | 查询状态 | `check_po_status` | Wrapper |

---

## 错误处理

| 情况 | 处理 |
|------|------|
| 备件不在清单 | 告知用户，询问正确型号/PN |
| 全部 OK | 直接报告"库存充足，无需补货" |
| Funding 不足 | 告知差额，给选项（减量/特殊审批/取消） |
| create_po 失败 | 重试 1 次，仍失败则告知手动处理 |
| 通知发送失败 | 报告中标注"通知未送达" |

---

## 扩展点（MVP 后）

- 价格查询接真实系统
- 审批自动跟踪 + 催办
- 到货自动更新库存
- 备件消耗预测 → 提前生成补货计划
- 历史消耗分析 → 优化 min_stock 设定
