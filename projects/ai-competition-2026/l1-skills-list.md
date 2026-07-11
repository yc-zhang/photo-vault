# GTD L1 Do-Thing Skill 全量清单

> 更新时间：2026-07-05
> 飞书 CLI：`@larksuite/cli` v1.0.65 + 27 个 OpenClaw Skill
> 总计：**~140 个 L1 Skill**

---

## 飞书 CLI Skill（✅ 真实可用 — 107 个）

### 即时通讯 / lark-im（13）

| # | Skill | 能力 |
|---|-------|------|
| 1 | `im_send` | 发送飞书消息（文本/Markdown/图片/文件/卡片） |
| 2 | `im_reply` | 回复消息（支持话题） |
| 3 | `im_send_card` | 发送交互卡片（按钮/表单/选择器） |
| 4 | `im_search_messages` | 搜索历史消息 |
| 5 | `im_list_chats` | 列出群聊/私聊 |
| 6 | `im_create_chat` | 创建群聊（群/话题模式） |
| 7 | `im_chat_members` | 管理群成员（增删/查） |
| 8 | `im_chat_search` | 按关键词搜群 |
| 9 | `im_reactions` | 表情回复（添加/删除/查询） |
| 10 | `im_forward` | 转发/合并转发消息 |
| 11 | `im_pin` | 置顶消息 |
| 12 | `im_urgent` | 加急（应用内/短信/电话） |
| 13 | `im_download_resource` | 下载消息中的图片/文件 |

### 邮件 / lark-mail（7）

| # | Skill | 能力 |
|---|-------|------|
| 14 | `mail_send` | 发送邮件 |
| 15 | `mail_read` | 读取/搜索邮件 |
| 16 | `mail_reply` | 回复/转发邮件 |
| 17 | `mail_draft` | 草稿管理 |
| 18 | `mail_watch` | 监听新邮件 |
| 19 | `mail_signature` | 邮件签名管理 |
| 20 | `mail_template` | 邮件模板 |

### 日历 / lark-calendar（5）

| # | Skill | 能力 |
|---|-------|------|
| 21 | `calendar_agenda` | 查看日程安排 |
| 22 | `calendar_create` | 创建日程/会议 |
| 23 | `calendar_search` | 搜索日程 |
| 24 | `calendar_room` | 查询/预定会议室 |
| 25 | `calendar_freebusy` | 查询忙闲 |

### 任务/看板 / lark-task（12）

| # | Skill | 能力 |
|---|-------|------|
| 26 | `task_create` | 创建任务 |
| 27 | `task_get` | 查看任务详情 |
| 28 | `task_update` | 更新任务（状态/描述/字段） |
| 29 | `task_complete` | 完成任务 |
| 30 | `task_reopen` | 重新打开任务 |
| 31 | `task_assign` | 分配成员 |
| 32 | `task_set_ancestor` | 设置父子任务（拆子任务） |
| 33 | `task_get_my_tasks` | 获取我的任务（按状态/优先级/截止日筛选） |
| 34 | `task_search` | 搜索任务 |
| 35 | `task_tasklist_create` | 创建任务清单 |
| 36 | `task_upload_attachment` | 上传任务附件 |
| 37 | `task_comment` | 任务评论 |

### 审批 / lark-approval（9）

| # | Skill | 能力 |
|---|-------|------|
| 38 | `approval_search` | 搜索可发起审批定义 |
| 39 | `approval_initiate` | 发起审批实例 |
| 40 | `approval_get` | 查询审批实例详情/进度/操作记录 |
| 41 | `approval_cancel` | 撤销审批 |
| 42 | `approval_tasks_query` | 查询待审批/已审批任务 |
| 43 | `approval_tasks_approve` | 通过审批 |
| 44 | `approval_tasks_reject` | 驳回审批 |
| 45 | `approval_tasks_transfer` | 转交审批 |
| 46 | `approval_tasks_remind` | 催办审批 |

### 云文档 / lark-doc（6）

| # | Skill | 能力 |
|---|-------|------|
| 47 | `doc_fetch` | 读取文档内容 |
| 48 | `doc_create` | 创建文档 |
| 49 | `doc_update` | 编辑文档 |
| 50 | `doc_md` | Markdown 格式读写 |
| 51 | `doc_media` | 插入/下载文档图片 |
| 52 | `doc_history` | 文档版本历史 |

### 电子表格 / lark-sheets（7）

| # | Skill | 能力 |
|---|-------|------|
| 53 | `sheets_read` | 读取单元格数据 |
| 54 | `sheets_write` | 写入单元格（值/公式/样式） |
| 55 | `sheets_batch_update` | 批量操作 |
| 56 | `sheets_chart` | 创建图表 |
| 57 | `sheets_pivot` | 透视表 |
| 58 | `sheets_filter` | 筛选/条件格式 |
| 59 | `sheets_search_replace` | 查找替换 |

### 多维表格 / lark-base（6）

| # | Skill | 能力 |
|---|-------|------|
| 60 | `base_create` | 创建多维表格 |
| 61 | `base_field` | 字段管理（增删改） |
| 62 | `base_record` | 记录操作（CRUD/批量） |
| 63 | `base_view` | 视图/筛选 |
| 64 | `base_dashboard` | 仪表盘 |
| 65 | `base_form` | 表单管理 |

### 云盘 / lark-drive（6）

| # | Skill | 能力 |
|---|-------|------|
| 66 | `drive_upload` | 上传文件 |
| 67 | `drive_download` | 下载文件 |
| 68 | `drive_search` | 搜索文件 |
| 69 | `drive_folder` | 文件夹管理 |
| 70 | `drive_move` | 移动/复制 |
| 71 | `drive_import` | 导入 Word/Excel/Markdown → 飞书在线文档 |

### 考勤 / lark-attendance（1）

| # | Skill | 能力 |
|---|-------|------|
| 72 | `attendance_query` | 查询打卡记录 |

### 视频会议 / lark-vc（5）

| # | Skill | 能力 |
|---|-------|------|
| 73 | `vc_search` | 搜索历史会议 |
| 74 | `vc_recording` | 获取录制/纪要/逐字稿 |
| 75 | `vc_agent_join` | 机器人加入进行中会议 |
| 76 | `vc_agent_events` | 读取会中实时事件 |
| 77 | `vc_agent_send` | 会中发送消息 |

### 妙记 / lark-minutes（4）

| # | Skill | 能力 |
|---|-------|------|
| 78 | `minutes_search` | 搜索妙记 |
| 79 | `minutes_detail` | 查看妙记详情/逐字稿/总结 |
| 80 | `minutes_upload` | 上传音视频转妙记 |
| 81 | `minutes_download` | 下载音视频文件 |

### 通讯录 / lark-contact（2）

| # | Skill | 能力 |
|---|-------|------|
| 82 | `contact_search` | 按姓名搜用户 |
| 83 | `contact_get` | 按 open_id 查用户详情 |

### 知识库 / lark-wiki（5）

| # | Skill | 能力 |
|---|-------|------|
| 84 | `wiki_space_list` | 列出知识空间 |
| 85 | `wiki_space_create` | 创建知识空间 |
| 86 | `wiki_node_create` | 在知识库创建文档节点 |
| 87 | `wiki_node_move` | 移动/复制节点 |
| 88 | `wiki_member` | 管理空间成员 |

### OKR / lark-okr（4）

| # | Skill | 能力 |
|---|-------|------|
| 89 | `okr_list` | 查看 OKR 列表 |
| 90 | `okr_create` | 创建目标/关键结果 |
| 91 | `okr_update` | 更新进度/指标 |
| 92 | `okr_align` | 管理对齐关系 |

### 幻灯片 / lark-slides（3）

| # | Skill | 能力 |
|---|-------|------|
| 93 | `slides_create` | 创建演示文稿 |
| 94 | `slides_get` | 读取幻灯片内容 |
| 95 | `slides_replace` | 替换幻灯片页面 |

### 画板 / lark-whiteboard（3）

| # | Skill | 能力 |
|---|-------|------|
| 96 | `whiteboard_query` | 查询画板内容 |
| 97 | `whiteboard_update` | 编辑画板 |
| 98 | `whiteboard_export` | 导出画板为图片 |

### 事件监听 / lark-event（1）

| # | Skill | 能力 |
|---|-------|------|
| 99 | `event_consume` | 实时消费飞书事件流（IM/任务/会议） |

### 妙搭应用 / lark-apps（4）

| # | Skill | 能力 |
|---|-------|------|
| 100 | `apps_create` | 创建飞书应用 |
| 101 | `apps_html_publish` | 发布 HTML 静态站点 |
| 102 | `apps_local_dev` | 本地全栈开发 |
| 103 | `apps_observability` | 日志/Trace/监控 |

### 其他（4）

| # | Skill | 能力 |
|---|-------|------|
| 104 | `lark-note` | 会议纪要详情/逐字稿直查 |
| 105 | `lark-markdown` | Markdown 文件创建/编辑/diff |
| 106 | `lark-openapi-explorer` | 查找未封装的飞书原生 API |
| 107 | `lark-shared` | 认证/权限/scope 管理 |

---

## 非飞书真实 Skill（2 个）

| # | Skill | 能力 | 来源 |
|---|-------|------|------|
| 108 | `send_email` | 发送邮件 | Gmail Skill（Maton API） |
| 109 | `read_email` | 读取/搜索邮件 | Gmail Skill（Maton API） |

---

## Wrapper API — Demo 模拟（29 个）

以下 L1 能力飞书原生不覆盖，需 Wrapper API mock。

### OGM / 采购（3）

| # | Skill | 能力 |
|---|-------|------|
| 110 | `query_funding` | 查询 OGM Funding 余额/流入/待花/Forecast |
| 111 | `create_po` | 创建采购单 |
| 112 | `check_po_status` | 查询采购单状态 |

### 备件 / Jobcard（3）

| # | Skill | 能力 |
|---|-------|------|
| 113 | `query_inventory` | 查询备件库存 |
| 114 | `query_jobcards` | 查询团队 Jobcard（谁忙谁闲） |
| 115 | `update_jobcard` | 更新 Jobcard 状态 |

### 承包商管理（2）

| # | Skill | 能力 |
|---|-------|------|
| 116 | `onboard_contractor` | 承包商入职：创建账号、分配权限、登记信息 |
| 117 | `offboard_contractor` | 承包商离职：回收权限、归档数据、注销账号 |

### 运维-设备（5）

| # | Skill | 能力 |
|---|-------|------|
| 118 | `list_devices` | 列出所有网络设备及基本信息 |
| 119 | `get_device_status` | 查询单设备实时状态（在线/离线/CPU/内存/温度） |
| 120 | `get_device_metrics` | 查询设备性能时序数据（带宽/丢包/延迟趋势） |
| 121 | `query_device_alerts` | 查询设备当前活跃告警 |
| 122 | `query_device_logs` | 查询设备操作/变更日志 |

### 运维-拓扑（1）

| # | Skill | 能力 |
|---|-------|------|
| 123 | `query_network_topology` | 查询网络拓扑（设备互联、链路状态） |

### 运维-工单（5）

| # | Skill | 能力 |
|---|-------|------|
| 124 | `create_ticket` | 创建工单（标题/分类/优先级/描述） |
| 125 | `get_ticket` | 查询工单详情和处理进度 |
| 126 | `assign_ticket` | 分配工单给处理人 |
| 127 | `update_ticket_status` | 更新工单状态并添加备注 |
| 128 | `close_ticket` | 关闭工单并记录解决方案 |

### 运维-故障（4）

| # | Skill | 能力 |
|---|-------|------|
| 129 | `declare_incident` | 声明故障事件（等级/影响范围/描述） |
| 130 | `update_incident` | 更新事件进展和处理动作 |
| 131 | `resolve_incident` | 关闭事件并记录根因 |
| 132 | `get_incident_timeline` | 查询事件处理全链路时间线 |

### 运维-统计（5）

| # | Skill | 能力 |
|---|-------|------|
| 133 | `get_device_availability` | 设备可用性 SLA 统计（uptime %） |
| 134 | `get_ticket_metrics` | 工单统计：数量/分布/平均处理时长 |
| 135 | `get_incident_metrics` | 事件统计：MTTR / MTBF / 频次趋势 |
| 136 | `get_traffic_report` | 流量/带宽使用报告 |
| 137 | `get_health_score` | 网络健康综合评分 |

### 工具类（1）

| # | Skill | 能力 |
|---|-------|------|
| 138 | `query_network_perf` | 查询网络带宽/延迟/可用性（实时快照） |

---

## 内部 Skill — Agent 框架（3 个）

| # | Skill | 能力 |
|---|-------|------|
| 139 | `skill_match` | 用户意图 → 模糊匹配 Domain Skill |
| 140 | `skill_orchestrate` | 按 Plan 编排执行 L1 Skill 链 |
| 141 | `schedule_cron` | 注册定时/周期任务 |

---

## 统计

| 分类 | 数量 | 状态 |
|------|------|------|
| 🟢 飞书 CLI | 107 | ✅ 真实可用 |
| 🟢 非飞书真实 | 2 | ✅ 真实可用 |
| 🟡 Wrapper API | 29 | ⏳ Demo 模拟 |
| 🔵 内部框架 | 3 | ✅ 框架自身 |
| **总计** | **141** | **真实率 79%** |
