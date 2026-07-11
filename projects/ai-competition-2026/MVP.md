# GTD MVP 定义

> 2026-07-08 与 Yuchen 讨论确定

---

## MVP 总览

三个场景，覆盖 4 个原始用例（#1 OGM 采购、#4 需求预测、#7 Jobcard、#8+9 网络），展示 GTD 从一句话触发到多步编排自动执行的完整能力。

---

## MVP 1：备件管理与采购（Spare Parts Management）

> 管理备件库存与状态，自动生成补货计划；库存不足时通过 OGM 资金启动采购。

**Skill:** `spare_parts_management` / Display: Spare Parts Management

**触发：** 「备件库存怎么样？」、「生成补货计划」、「采购 X 备件」

### 三段式流程

```
Phase 1: 库存感知
  备件库库存 ──→ 现网库存 ──→ 库存状态分析
                                    │
Phase 2: 补货决策                   ▼
  缺口计算 ──→ 补货计划生成 ──→ 用户确认
                                    │
Phase 3: 采购执行（仅需补货时触发）   ▼
  查 Funding ──→ 预算判断 ──→ 生成采购单 ──→ 通知 Siru ──→ 创建跟进任务
```

### 需要的 L1 Skill

| Phase | 步骤 | L1 Skill | 来源 |
|-------|------|---------|------|
| P1 | 查备件库库存 | `query_inventory --location spare_parts` | Wrapper API |
| P1 | 查现网库存 | `query_inventory --location field` | Wrapper API |
| P2 | 缺口计算 & 补货计划 | 业务逻辑（L2 层） | — |
| P3 | 查 Funding 余额 | `query_funding` | Wrapper API |
| P3 | 生成采购单 | `create_po` | Wrapper API |
| P3 | 通知采购同事 | `im_send` | ✅ 飞书 |
| P3 | 跟进结果 | `check_po_status` + `task_create` | Wrapper + ✅ 飞书 |

### 展示要点
- 库存感知 → 补货决策 → 采购执行，三段清晰分离
- 用户可选择只看补货计划（不执行采购）
- 多步 L1 编排（展示 L2 价值）
- 跨系统协作（Wrapper API + 飞书）
- 同步 + 异步混合（主流程立刻返回，跟踪走异步）

---

## MVP 2：Jobcard 管理

> 每日盘点团队负载，自动分配新任务，发现阻塞和未 refine 的工作。

**触发：** 用户问「今天团队状态怎么样？」/ 定时每日触发

### 流程

```
每日盘点启动
      │
      ├─→ 查团队负载（谁忙谁闲）
      ├─→ 查休假情况
      ├─→ 新任务 → 匹配合适的人 → 邮件通知分配
      │
      ├─→ 未 Refine 的工作 → 列出需要拆分/细化/重构的
      │
      └─→ 被 Block 的工作 → 状态？能否 unblock？
```

### 需要的 L1 Skill

| 步骤 | L1 Skill | 来源 |
|------|---------|------|
| 查团队 Jobcard 负载 | `query_jobcards` | Wrapper API |
| 查休假情况 | `calendar_freebusy` / `calendar_agenda` | ✅ 飞书 |
| 匹配人员 | 业务逻辑（L2 层判断） | — |
| 邮件通知分配 | `mail_send` | ✅ 飞书 / Gmail |
| 查未 Refine 工作 | `query_jobcards`（过滤） | Wrapper API |
| 查 Blocked 工作 | `query_jobcards`（过滤） | Wrapper API |
| 更新 Jobcard | `update_jobcard` | Wrapper API |

### 展示要点
- 团队运营自动化（不是技术运维，是管理场景）
- 飞书日历 + Wrapper 的数据融合
- 从分析到行动的闭环（发现问题 → 分配人 → 通知到位）

---

## MVP 3：实时网络状态 & 团队运营汇报

> Merge 了原始用例 #8（网络测试）和 #9（网络性能汇报），从即时查询到定时报表全覆盖。

**触发：** 用户问「现在网络怎么样？」/ 定时每日/每周触发

### 流程

```
用户问"现在网络怎么样？" / 定时触发
      │
      ├─→ 实时网络状态
      │     ├─ 有线办公网
      │     ├─ 无线（办公 / 酒店）
      │     ├─ 专线状态
      │     ├─ 海外访问路径
      │     └─ SaaS 延迟（常用几个）
      │
      ├─→ 运营概况
      │     ├─ 有无 incident
      │     ├─ 今日 change 数量（待批 / 被打回）
      │     └─ 特殊事件支持（董事会、周年庆、VIP）
      │
      └─→ 生成报表 → IM 确认 → 邮件发送存档
```

### 需要的 L1 Skill

| 步骤 | L1 Skill | 来源 |
|------|---------|------|
| 网络延迟/带宽 | `query_network_perf` / 真实 CLI | Wrapper + 宿主机 |
| 设备状态 | `get_device_status` | Wrapper API |
| 查询告警 | `query_device_alerts` | Wrapper API |
| 查询 incident | `get_incident_metrics` | Wrapper API |
| 查询 change | `get_ticket_metrics` | Wrapper API |
| 特殊事件 | `calendar_agenda`（搜关键词） | ✅ 飞书 |
| 生成报表 | 业务逻辑 + 文本拼接 | — |
| IM 确认 | `im_send`（卡片确认） | ✅ 飞书 |
| 邮件发送 | `mail_send` | ✅ 飞书 / Gmail |

### 展示要点
- 真枪实弹调宿主机 CLI（不是 mock）
- 三个调度模式全展示：On-demand（用户问） + Scheduled（定时报表） + Event-driven（告警触发）
- IM 确认 → 邮件存档的 double-check 流程

---

## Wrapper API 汇总

三个 MVP 共需 **11 个 Wrapper API**（从原计划 29 个精简）：

| Wrapper API | MVP 1 | MVP 2 | MVP 3 |
|-------------|:-----:|:-----:|:-----:|
| `query_inventory` | ✅ | | |
| `query_funding` | ✅ | | |
| `create_po` | ✅ | | |
| `check_po_status` | ✅ | | |
| `query_jobcards` | | ✅ | |
| `update_jobcard` | | ✅ | |
| `query_network_perf` | | | ✅ |
| `get_device_status` | | | ✅ |
| `query_device_alerts` | | | ✅ |
| `get_ticket_metrics` | | | ✅ |
| `get_incident_metrics` | | | ✅ |

---

## 不在 MVP 范围

| 场景 | 原因 |
|------|------|
| 采购咨询 | MVP 1 已包含通知采购同事流程 |
| 北美保修 | 邮件自动跟进模式与 MVP 1 类似，不做重复 Demo |
| 流程自动化 | 优先级低，MVP 后迭代 |
| Skill 依赖图谱 | 开发工具，非路演展示内容 |
| 特殊事件保障 | MVP 3 已包含特殊事件检测 |
| Docker 容器化 | MVP 阶段先不容器化 |
| O2 路演完整 PPT | 配合 MVP 先做大纲 |
