# 2026 AI Competition — PatternMaker

> 把重复消灭在源头的人。

---

## 基本信息

- **竞赛：** 2026 AI Competition
- **队名：** PatternMaker
- **队长：** Yuchen Zhang (yuchen.zhang@disney.com)
- **队员：** Allen Zhou, Daniel Hu, Qingquan Gu, Robinson Zhang, Shenwei Jiang, Kenny Lin X
- **时间线：** 备战 7–10 月，决赛 10 月下旬路演

---

## 团队分工

- **Yuchen：** 架构设计 + Agent 核心实现 + 路演
- **其他队员：** Domain Knowledge Provider — 将各自领域知识转化为 Skills（设定模式 → 模糊匹配 → 现成工作流执行）

---

## 两个目标

### O1 — Agent for Daily Operations

在我家的 MacBook Pro 上跑一个 Agent，目标是为 T&D 整个部门提效。

#### 范围

- **IM 对话：** ✅ 已集成飞书，用户在 IM 里说话 → Agent 回应
- **邮件：** ✅ 已有 Gmail Skill（Maton API），可收发
- **数据：** 全部 Dummy / Demo 数据，不接真实系统
- **Wrapper API：** 模拟后端系统，假装接了（Fake it until we make it）
- **核心验证：** IM 入口 → 模糊匹配 Domain Skill → 编排 L1 → 返回结果

#### 不做的

- 真实系统接入（业务后端；飞书已真实接入）
- 生产环境部署
- 权限/安全体系（飞书 bot-only 已覆盖基础安全）
- OGM/运维等非飞书系统的真实后端（仍有 Wrapper API demo）

### O2 — Presentation & Roadshow

HTML Deck + 路演 Script。

- 完整的 presentation 大纲
- 讲故事 + 实现展示 + Demo
- **重点体现每个 team member 的贡献**
- **核心叙事：** 用我的一天（without GTD）vs 用 GTD 的一天（with GTD），对比效率提升
- 参考：https://claude.com/resources/tutorials/using-claude-design-for-presentations-and-slide-decks

---

## 项目命名

**项目名：** GetThingsDone（简称 GTD）

**核心概念：** 简单直接 — 把事儿干了。做一个 Agent，让 T&D 的同事们可以每天使用。让 Agent 替人做事情，而不是替人思考。

### One-liner

> **GTD** — An AI agent that runs on your Mac, lives in your IM, and gets your daily IT operations done. So you don't have to.

### Pitch

> **Before GTD:** You ask ChatGPT → it tells you how → you still do the work.
> **After GTD:** You ask GTD → it does the work → you get the result.
>
> GTD turns your AI from a thinker into a doer. For IT teams drowning in routine, that's not an upgrade — it's a new category.

### 范式转变

**Before：**
```
人 → Natural Language → LLM
LLM → Response → 人（受到启迪后）→ Do things
（循环）
```

**After：**
```
人 → Natural Language → Agent → LLM / MaaS → Do things → Result → 人
|______________________________|
      我们要封装的部分
```

- **「人 → Natural Language → Agent」** → 用 IM 搞定（演示用飞书）
- **「Agent → LLM / MaaS → Do things」** → 核心实现
- **「Result → 人」** → 多种通知方式：邮件、IM、内部沟通、系统记录…总之告诉 invoker：the job is DONE

---

## 用例脑暴

| # | 场景 | 描述 |
|---|------|------|
| 1 | OGM 备件采购 | 管理 OGM Funding（资金流入、待花、Forecast） |
| 2 | 采购咨询 | 找 Siru 处理采购问题 |
| 3 | 北美保修 | 写简单邮件问同事，等待结果跟进 |
| 4 | 备件需求预测 | 根据现网数据推断备件需求并发起流程 |
| 5 | 流程自动化 | 报备、登记、出勤管理 |
| 6 | Skill 依赖图谱 | 画出 Skill 之间的依赖关系 |
| 7 | Jobcard 管理 | 大家都在忙什么？谁有空？谁很忙？ |
| 8 | 网络测试 | 测试带宽、测试延迟 |
| 9 | 网络性能汇报 | 实时汇报网络性能 |
| 10 | 特殊事件保障 | 如 10 周年等突发事件支持 |

---

## 功能设计

传统产品设计：先想功能，再做规划。

GTD 不同 — Agent 的「功能」即 **Skill**。Agent 通过组合不同的 Skill 来实现目标。

### Skill 的两层模型

| 层级 | 类型 | 职责 | 谁提供 |
|------|------|------|--------|
| **L1: Do-Thing Skill** | 执行层 | 原子操作：发邮件、查系统、测网络、建工单… | Yuchen（基础设施） |
| **L2: Domain Skill** | 编排层 | 知道业务逻辑，按场景调用 L1 Skill 完成任务 | Team Members（领域知识） |

**核心理念：**

- L2（Domain Skill）= Business Knowledge + Orchestration
- L2 不直接做事，它是「知道该做什么、按什么顺序做」的那层
- L2 调用 L1 去执行

**举例：**

> 用户：「帮我处理 OGM 备件采购」
>
> **Domain Skill（L2）** 知道这个业务流程：
> 1. 查 OGM Funding 余额 → 调用 L1 `query_funding`
> 2. 判断是否在预算内 → 业务逻辑
> 3. 生成采购单 → 调用 L1 `create_po`
> 4. 通知 Siru → 调用 L1 `send_message`
> 5. 跟踪状态 → 调用 L1 `check_po_status`
>
> 用户不需要知道这些步骤 — Domain Skill 封装了这一切。

### 对应团队分工

- **Yuchen：** 搭建 L1 Skill 基础设施 + Agent 框架（让 L2 能跑起来）
- **Team Members：** 各自贡献 L2 Domain Skill（OGM、保修、Jobcard、网络…）
- **PatternMaker 哲学：** 每个队员把自己的领域知识 codify 成 Pattern → 模糊匹配触发 → Agent 自动执行
- **实施路径：** Yuchen 先写一个 L2→L1 全套 reference Skill（样板），队员照此模式填自己的领域知识

### Skill 设计准则

#### 1. 粒度准则

| L1 Do-Thing | L2 Domain |
|-------------|-----------|
| 原子操作，单一职责 | 完整业务意图，一次对话触发 |
| 一个 Skill = 一件事 | 一个 Skill = 一个业务场景 |
| 例：`send_email`、`query_db` | 例：`ogm_procurement`、`warranty_inquiry` |

**原则：** L1 不包含业务判断。L2 不直接操作外部系统。

#### 2. 执行模式

| 模式 | 场景 | 示例 |
|------|------|------|
| **Sync（同步）** | 即时查询、快速操作 | 「现在 OGM 余额多少？」 |
| **Async（异步）** | 多步骤、依赖外部、等待回复 | 「帮我发邮件问北美保修，有回复告诉我」 |

**原则：** 用户说完话 5 秒内能完成的 → Sync。需要等外部系统/人等 → Async。Async 必须有 callback/notification 机制。

#### 3. 调度模式

| 模式 | 触发方式 | 示例 |
|------|---------|------|
| **On-demand** | 用户在 IM 里说一句话 | 「测试一下现在的网络延迟」 |
| **Scheduled** | Cron / 定时触发 | 「每天早上 9 点发网络性能报告」 |
| **Event-driven** | 外部事件触发（✅ lark-event 已就绪） | 「收到审批请求时自动提醒」「新邮件抵达时触发处理」 |

**原则：** Scheduled 和 Event-driven 本质上是「Domain Skill + 触发器」。Skill 本身不变，只是触发方式不同。lark-event 提供了真实的飞书事件流作为 event-driven 触发器。

#### 4. 上下文准则

每个 Skill 有明确的上下文边界：

- **输入：** 明确声明需要哪些参数（用户输入的 + 从 L1 获取的）
- **输出：** 明确声明返回什么（给用户的 + 给下一个 Skill 的）
- **Token 预算：** Skill 执行有上下文上限，不把巨型数据塞进 prompt
- **状态传递：** L2 编排 L1 时，L1 的输出经过裁剪后再传给下一个 L1

#### 5. I/O 契约

```
L1 Skill 接口：
  输入  { params: {...}, context: {...} }
  输出  { success: bool, data: any, error?: string }

L2 Skill 接口：
  输入  { user_intent: string, user_context: {...} }
  输出  { plan: Step[], result_summary: string }
```

**原则：** L1 全部遵循统一接口 → L2 可以自由编排任意 L1 → 组合爆炸。这才是 PatternMaker 的核心能力。

#### 6. Skill 注册与发现

- 每个 Skill（L1 & L2）需注册：名称、描述、输入输出 schema、执行模式（sync/async）、标签
- Agent 通过**模糊匹配**用户意图 → Skill 描述 → 找到对应的 Domain Skill
- Domain Skill 描述越清晰，匹配越准确

---

## L1 Do-Thing Skill 清单

GTD 的 L1 层是原子操作集合。分为三类：**真实飞书 CLI Skill**（已安装可用）、**其他真实 Skill**、**Wrapper API**（Demo 模拟）。

### 飞书 CLI L1 Skill（✅ 真实可用 — 2026-07-05 已安装）

通过 `@larksuite/cli` v1.0.65 + 27 个 OpenClaw Skill，飞书全线能力已就绪。

#### 即时通讯（lark-im）

| Skill | 能力 | 对应原 Wrapper |
|-------|------|---------------|
| `im_send` | 发送飞书消息（文本/Markdown/图片/文件/卡片） | → 替代 `send_im`、`notify_user` |
| `im_reply` | 回复消息（支持话题） | — |
| `im_send_card` | 发送交互卡片（按钮/表单/选择器） | — |
| `im_search_messages` | 搜索历史消息 | — |
| `im_list_chats` | 列出群聊/私聊 | — |
| `im_create_chat` | 创建群聊（群/话题模式） | — |
| `im_chat_members` | 管理群成员（增删/查） | — |
| `im_chat_search` | 按关键词搜群 | — |
| `im_reactions` | 表情回复（添加/删除/查询） | — |
| `im_forward` | 转发/合并转发消息 | — |
| `im_pin` | 置顶消息 | — |
| `im_urgent` | 加急（应用内/短信/电话） | — |
| `im_download_resource` | 下载消息中的图片/文件 | — |

#### 邮件（lark-mail）

| Skill | 能力 | 对应原 Skill |
|-------|------|-------------|
| `mail_send` | 发送邮件 | → 补充 `send_email`（Gmail 之外多一个通道） |
| `mail_read` | 读取/搜索邮件 | → 补充 `read_email` |
| `mail_reply` | 回复/转发邮件 | — |
| `mail_draft` | 草稿管理 | — |
| `mail_watch` | 监听新邮件 | → Async 回调能力 |
| `mail_signature` | 邮件签名管理 | — |
| `mail_template` | 邮件模板 | — |

#### 日历（lark-calendar）

| Skill | 能力 | 对应原 Wrapper |
|-------|------|---------------|
| `calendar_agenda` | 查看日程安排 | → 替代 `query_calendar` |
| `calendar_create` | 创建日程/会议 | — |
| `calendar_search` | 搜索日程 | — |
| `calendar_room` | 查询/预定会议室 | — |
| `calendar_freebusy` | 查询忙闲 | — |

#### 任务/看板（lark-task）

| Skill | 能力 | 对应原 Wrapper |
|-------|------|---------------|
| `task_create` | 创建任务 | → 替代 `create_task` |
| `task_get` | 查看任务详情 | → 替代 `get_task` |
| `task_update` | 更新任务 | → 替代 `update_task`、`move_task`、`block_task`、`unblock_task` |
| `task_complete` | 完成任务 | — |
| `task_reopen` | 重新打开任务 | — |
| `task_assign` | 分配成员 | → 替代 `assign_task` |
| `task_set_ancestor` | 设置父子任务 | → 替代 `split_task`、`list_subtasks` |
| `task_get_my_tasks` | 获取我的任务 | → 替代 `list_tasks`、`query_overdue_tasks` |
| `task_search` | 搜索任务 | — |
| `task_tasklist_create` | 创建任务清单 | — |
| `task_upload_attachment` | 上传任务附件 | — |
| `task_comment` | 任务评论 | — |

#### 审批（lark-approval）

| Skill | 能力 | 对应原 Wrapper |
|-------|------|---------------|
| `approval_search` | 搜索可发起审批定义 | → 替代 `list_approval_templates`、`get_approval_template` |
| `approval_initiate` | 发起审批实例 | → 替代 `submit_approval` |
| `approval_get` | 查询审批实例详情 | → 替代 `query_approval` |
| `approval_cancel` | 撤销审批 | → 替代 `cancel_approval` |
| `approval_tasks_query` | 查询待审批/已审批任务 | — |
| `approval_tasks_approve` | 通过审批 | → 替代 `approve_task` |
| `approval_tasks_reject` | 驳回审批 | → 替代 `reject_task` |
| `approval_tasks_transfer` | 转交审批 | → 替代 `transfer_task` |
| `approval_tasks_remind` | 催办审批 | — |

#### 云文档（lark-doc）

| Skill | 能力 | 对应原 Skill |
|-------|------|-------------|
| `doc_fetch` | 读取文档内容 | → 增强 `feishu_doc` |
| `doc_create` | 创建文档 | — |
| `doc_update` | 编辑文档 | — |
| `doc_md` | Markdown 格式读写 | — |
| `doc_media` | 插入/下载文档图片 | — |
| `doc_history` | 文档版本历史 | — |

#### 电子表格（lark-sheets）

| Skill | 能力 |
|-------|------|
| `sheets_read` | 读取单元格数据 |
| `sheets_write` | 写入单元格（值/公式/样式） |
| `sheets_batch_update` | 批量操作 |
| `sheets_chart` | 创建图表 |
| `sheets_pivot` | 透视表 |
| `sheets_filter` | 筛选/条件格式 |
| `sheets_search_replace` | 查找替换 |

#### 多维表格（lark-base）

| Skill | 能力 |
|-------|------|
| `base_create` | 创建多维表格 |
| `base_field` | 字段管理（增删改） |
| `base_record` | 记录操作（CRUD/批量） |
| `base_view` | 视图/筛选 |
| `base_dashboard` | 仪表盘 |
| `base_form` | 表单管理 |

#### 云盘（lark-drive）

| Skill | 能力 |
|-------|------|
| `drive_upload` | 上传文件 |
| `drive_download` | 下载文件 |
| `drive_search` | 搜索文件 |
| `drive_folder` | 文件夹管理 |
| `drive_move` | 移动/复制 |
| `drive_import` | 导入 Word/Excel/Markdown → 飞书在线文档 |

#### 考勤（lark-attendance）

| Skill | 能力 | 对应原 Wrapper |
|-------|------|---------------|
| `attendance_query` | 查询打卡记录 | → 替代 `register_attendance`（查询端） |

#### 视频会议（lark-vc / lark-vc-agent）

| Skill | 能力 |
|-------|------|
| `vc_search` | 搜索历史会议 |
| `vc_recording` | 获取录制/纪要/逐字稿 |
| `vc_agent_join` | 机器人加入进行中会议 |
| `vc_agent_events` | 读取会中实时事件 |
| `vc_agent_send` | 会中发送消息 |

#### 妙记（lark-minutes）

| Skill | 能力 |
|-------|------|
| `minutes_search` | 搜索妙记 |
| `minutes_detail` | 查看妙记详情/逐字稿/总结 |
| `minutes_upload` | 上传音视频转妙记 |
| `minutes_download` | 下载音视频文件 |

#### 通讯录（lark-contact）

| Skill | 能力 |
|-------|------|
| `contact_search` | 按姓名搜用户 |
| `contact_get` | 按 open_id 查用户详情 |

#### 知识库（lark-wiki）

| Skill | 能力 |
|-------|------|
| `wiki_space_list` | 列出知识空间 |
| `wiki_space_create` | 创建知识空间 |
| `wiki_node_create` | 在知识库创建文档节点 |
| `wiki_node_move` | 移动/复制节点 |
| `wiki_member` | 管理空间成员 |

#### OKR（lark-okr）

| Skill | 能力 |
|-------|------|
| `okr_list` | 查看 OKR 列表 |
| `okr_create` | 创建目标/关键结果 |
| `okr_update` | 更新进度/指标 |
| `okr_align` | 管理对齐关系 |

#### 幻灯片（lark-slides）

| Skill | 能力 |
|-------|------|
| `slides_create` | 创建演示文稿 |
| `slides_get` | 读取幻灯片内容 |
| `slides_replace` | 替换幻灯片页面 |

#### 画板（lark-whiteboard）

| Skill | 能力 |
|-------|------|
| `whiteboard_query` | 查询画板内容 |
| `whiteboard_update` | 编辑画板 |
| `whiteboard_export` | 导出画板为图片 |

#### 事件监听（lark-event）

| Skill | 能力 |
|-------|------|
| `event_consume` | 实时消费飞书事件流（IM/任务/会议） | → Event-driven 调度的真实实现 |

#### 妙搭应用（lark-apps）

| Skill | 能力 |
|-------|------|
| `apps_create` | 创建飞书应用 |
| `apps_html_publish` | 发布 HTML 静态站点 |
| `apps_local_dev` | 本地全栈开发 |
| `apps_observability` | 日志/Trace/监控 |

#### 其他

| Skill | 能力 |
|-------|------|
| `lark-note` | 会议纪要详情/逐字稿直查 |
| `lark-markdown` | Markdown 文件创建/编辑/diff |
| `lark-openapi-explorer` | 查找未封装的飞书原生 API |
| `lark-shared` | 认证/权限/scope 管理 |

### 已有（非飞书）真实 Skill

| Skill | 能力 | 来源 |
|-------|------|------|
| `send_email` | 发送邮件 | Gmail Skill（Maton API） |
| `read_email` | 读取/搜索邮件 | Gmail Skill（Maton API） |

### Wrapper API（Demo 模拟 — 无飞书对应）

以下 L1 能力飞书原生不覆盖，需 Wrapper API 模拟。

| Skill | 模拟的能力 | 对应用例 |
|-------|-----------|---------|
| `query_funding` | 查询 OGM Funding 余额、流入、待花、Forecast | OGM 备件采购 |
| `create_po` | 创建采购单 | OGM 备件采购 |
| `check_po_status` | 查询采购单状态 | OGM 备件采购 |
| `query_inventory` | 查询备件库存 | 备件需求预测 |
| `query_jobcards` | 查询团队 Jobcard（谁忙谁闲） | Jobcard 管理 |
| `update_jobcard` | 更新 Jobcard 状态 | Jobcard 管理 |
| `onboard_contractor` | 承包商入职：创建账号、分配权限、登记信息 | 承包商管理 |
| `offboard_contractor` | 承包商离职：回收权限、归档数据、注销账号 | 承包商管理 |
| `list_devices` | 列出所有网络设备及其基本信息 | 运维-设备 |
| `get_device_status` | 查询单设备实时状态（在线/离线/CPU/内存/温度） | 运维-设备 |
| `get_device_metrics` | 查询设备性能时序数据（带宽/丢包/延迟趋势） | 运维-设备 |
| `query_device_alerts` | 查询设备当前活跃告警 | 运维-设备 |
| `query_device_logs` | 查询设备操作/变更日志 | 运维-设备 |
| `query_network_topology` | 查询网络拓扑（设备互联、链路状态） | 运维-设备 |
| `create_ticket` | 创建工单（标题/分类/优先级/描述） | 运维-工单 |
| `get_ticket` | 查询工单详情和处理进度 | 运维-工单 |
| `assign_ticket` | 分配工单给处理人 | 运维-工单 |
| `update_ticket_status` | 更新工单状态并添加备注 | 运维-工单 |
| `close_ticket` | 关闭工单并记录解决方案 | 运维-工单 |
| `declare_incident` | 声明故障事件（等级/影响范围/描述） | 运维-故障 |
| `update_incident` | 更新事件进展和处理动作 | 运维-故障 |
| `resolve_incident` | 关闭事件并记录根因 | 运维-故障 |
| `get_incident_timeline` | 查询事件处理全链路时间线 | 运维-故障 |
| `get_device_availability` | 设备可用性 SLA 统计（uptime %） | 运维-统计 |
| `get_ticket_metrics` | 工单统计：数量/分布/平均处理时长 | 运维-统计 |
| `get_incident_metrics` | 事件统计：MTTR / MTBF / 频次趋势 | 运维-统计 |
| `get_traffic_report` | 流量/带宽使用报告 | 运维-统计 |
| `get_health_score` | 网络健康综合评分 | 运维-统计 |

### 工具类（Utilities）

| Skill | 能力 | 用例 |
|-------|------|------|
| `query_network_perf` | 查询网络带宽/延迟/可用性（实时快照） | 网络测试 |

### 内部 Skill（Agent 框架自身）

| Skill | 能力 |
|-------|------|
| `skill_match` | 用户意图 → 模糊匹配 Domain Skill |
| `skill_orchestrate` | 按 Plan 编排执行 L1 Skill 链 |
| `schedule_cron` | 注册定时/周期任务 |

> **设计原则：** Wrapper API 接口与真实 API 完全一致。未来只需替换 endpoint，L2 Domain Skill 无需改动。
>
> **飞书 CLI 集成（2026-07-05）：** `@larksuite/cli` v1.0.65 已安装，27 个 OpenClaw Skill 覆盖 IM / 邮件 / 日历 / 任务 / 审批 / 文档 / 表格 / 云盘 / 考勤 / 会议 / 妙记 / 通讯录 / 知识库 / OKR / 幻灯片 / 画板 / 事件监听。飞书 L1 层无需 Wrapper 模拟，全是真实 API 调用。
>
> **三层 L1 结构：** 飞书 CLI Skill（真实） + 其他真实 Skill（Gmail 等） + Wrapper API（非飞书系统 demo）。飞书系占 L1 总量的 ~60%，且全部真实可用。Event-driven 调度（lark-event）和定时调度（lark-task 轮询 / cron）均已有真实实现路径。

---

## 架构设计

### 架构总览

```
┌──────────────────────────────────────┐
│            Docker Container           │
│                                      │
│  ┌────────────────────────────────┐  │
│  │        GTD Skills Pack          │  │
│  │   L2 Domain  │  L1 Do-Thing    │  │
│  └──────────────┴─────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │     OpenClaw (Agent Platform)   │  │
│  │   • IM Gateway (飞书)           │  │
│  │   • Skill Registry & Match     │  │
│  │   • LLM Gateway                 │  │
│  └────────────────────────────────┘  │
│                                      │
│  ┌────────────────────────────────┐  │
│  │   Host Environment              │  │
│  │   • CLI (curl, ffmpeg, ...)    │  │
│  │   • SDK (Python, Node.js)      │  │
│  │   • Wrapper API (mock servers) │  │
│  └────────────────────────────────┘  │
│                                      │
│  LLM: DeepSeek  │  MaaS: TBD         │
└──────────────────────────────────────┘
```

**核心原则：**
- **OpenClaw 是底盘** — 不重复造轮子，消息路由、Skill 注册、LLM Gateway 全部复用
- **GTD 是上层建筑** — 一组 Skills + 宿主机工具链
- **Docker 封装一切** — CLI 依赖、SDK 版本、Wrapper API 全部打包，一键部署
- **MaaS 待定** — 多模态能力还在考察

### 关键架构决策

> 待 Yuchen 决策

#### 1. Skill 注册与匹配
- L1/L2 Skill 如何被发现和匹配？
- ✅ 飞书 L1 使用 OpenClaw 原生 Skill 系统（27 个已安装注册，`~/.agents/skills/lark-*`）
- GTD L2 Domain Skill 也用 OpenClaw Skill 体系注册，与 L1 同频
- 模糊匹配：L2 Skill 通过 description 和标签被 Agent 自动匹配

#### 2. 编排引擎
- L2 Skill 的执行流程是**预定义 plan**（写死的步骤），还是**LLM 动态生成 plan**？
- Async 任务（等邮件回复那种）怎么挂起和恢复？

#### 3. Wrapper API 实现
- 本地 HTTP mock server（如 json-server）？还是直接在 Node/Python 函数里 return dummy data？
- 接口规范：REST？还是函数调用？
- ⚡ 飞书系 L1 无需 Wrapper — 全部真实调用。Wrapper API 仅剩 ~15 个非飞书领域（OGM、工单、运维、承包商管理）

#### 4. Docker 化策略
- OpenClaw 本身已有 Docker 方案还是需要自己写 Dockerfile？
- 目标平台：macOS（开发）→ Linux（部署）？
- M1/M2 ARM 兼容？

#### 5. MaaS 选型
- 多模态能力（图片理解、语音、视频）用什么？
- 候选：GPT-4o、Claude、通义千问、StepFun？

#### 6. 状态持久化
- Async 任务状态存哪里？（SQLite？文件？OpenClaw 内置？）
- 用户会话上下文保留多久？

---

## 实现计划

### O1 计划
- TBD

### O2 计划
- TBD

---

## 价值主张

用数字说话，特别是在 O2 中体现量化价值。

- Storytelling 怎么做？
- 如何量化提效成果？

---

## 待决策事项

- [x] 项目名 → **GetThingsDone (GTD)**
- [ ] O1 MVP 范围定义
- [ ] O2 Presentation 大纲
- [ ] 架构设计文档
- [ ] Yuchen 先做 Skill Demo（L1 + L2 全套样板）→ 队员照此模式贡献领域知识
- [ ] 价值量化指标
