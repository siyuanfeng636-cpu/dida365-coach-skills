# 通用任务管理流程

## 目标

承接非教练型但高频的滴答清单操作，包括：

- 查询今天的任务或某段时间的任务
- 查看清单或项目
- 按条件筛选任务
- 创建普通任务
- 更新提醒、优先级、截止时间、标签
- 标记任务完成
- 移动任务到其他清单

## 交互原则

- 查询类请求直接读取并告诉用户结果，不要把查询也变成确认流程。
- 单个明确写操作默认直接执行，执行前只用一句话说明准备做什么。
- 如果任务对象不清、范围不清，先问 1 个决定性问题，不要把字段一次性全问完。
- 完成通用任务请求后，最多补 1 条高价值建议，例如提醒缺失、优先级冲突或适合时间盒化。
- 如果用户只是要快速执行，建议压到一句可忽略的补充，不要喧宾夺主。
- 任务反馈、执行结果和状态汇报时，必须带上所属清单名称；如果是多条任务，优先按清单分组反馈，不要只报任务标题。

## 查询类请求

### 今天 / 明天 / 最近的任务

优先流程：

1. 用 `dida project list --json` 收集清单 ID
2. 用 `dida task filter --projects <ids> --start-date <iso> --end-date <iso> --status 0 --json`
3. 需要看已完成时，再补 `dida task completed --projects <ids> --start-date <iso> --end-date <iso> --json`

如果用户说“我今天有哪些任务”，不要只查未完成就当成全量清单；要说明当前返回的是未完成任务，或补查已完成任务。

输出时优先使用“清单名称 + 任务标题”的形式，避免用户分不清任务属于哪个清单。

### 指定日期范围

优先使用：

- 未完成：`dida task filter --projects <ids> --start-date <iso> --end-date <iso> --status 0 --json`
- 已完成：`dida task completed --projects <ids> --start-date <iso> --end-date <iso> --json`

### 清单 / 项目查看

优先使用：

- 所有清单：`dida project list --json`
- 清单详情：`dida project get <projectId> --json`
- 清单及任务：`dida project data <projectId> --json`

### 多条件筛选

优先使用：

- `dida task filter --projects <ids> --start-date <iso> --end-date <iso> --priority <levels> --status <codes> --tag <tags> --json`

适用于按日期、清单、优先级、标签、状态的组合筛选。

## 写操作请求

所有写操作都遵守这两个原则：

1. 先用一句话告诉用户准备执行什么
2. 执行后必须回读校验，不能只汇报“已完成”

只有高风险批量动作才需要显式确认：

- 批量完成
- 批量改期
- 一次移动多条任务
- 清空式或不可逆的大范围修改

### 创建任务

优先使用：

- `dida task create --title "<title>" --project <projectId> --json`

按请求补充：

- `--content`
- `--start-date`
- `--due-date`
- `--time-zone`
- `--reminders`
- `--priority`
- `--items`

创建后立刻：

- `dida task get <projectId> <taskId> --json`

必须校验：

- 标题
- 优先级
- 截止时间
- 提醒时间
- 清单归属

向用户回报创建结果时，要明确说出任务创建到了哪个清单。

### 更新任务

适用于：

- 改标题
- 改优先级
- 改截止时间
- 改提醒
- 改标签或内容

优先使用：

- `dida task update <taskId> --id <taskId> --project <projectId> ... --json`

更新后立刻：

- `dida task get <projectId> <taskId> --json`

如果回读后提醒仍等于截止时间，不能说“提前提醒已设置成功”。
如果更新后任务仍在原清单或已移动到新清单，也要在反馈里明确报出清单名称。

### 完成任务

优先使用：

- `dida task complete <projectId> <taskId>`

完成后立刻：

- `dida task get <projectId> <taskId> --json`

如果是重复任务，回读时只信当前实例状态，不要把历史完成记录当成本次已完成。
向用户汇报完成结果时，至少说清任务标题和所属清单。

### 移动任务

优先使用：

- `dida task move --from <sourceProjectId> --to <destProjectId> --task <taskId>`

移动后立刻：

- `dida task get <destProjectId> <taskId> --json`
- 或 `dida project data <destProjectId> --json`

不要假设更新任务可以替代跨清单移动。
移动成功后，反馈里必须明确说出“从哪个清单移到哪个清单”。

## 用户表达到命令的推荐映射

- “我今天有哪些任务？” -> `dida project list --json` + `dida task filter ... --status 0 --json`
- “列出所有清单” -> `dida project list --json`
- “帮我创建一个任务” -> `dida task create ... --json`
- “把这个任务标记完成” -> `dida task complete <projectId> <taskId>`
- “把这个任务移到工作清单” -> `dida task move --from ... --to ... --task ...`
- “按优先级筛一下今天未完成任务” -> `dida task filter ... --priority 1,3,5 --status 0 --json`

## 约束

- 不要发明不存在的 CLI 子命令。
- 没有回读校验前，不要向用户确认“提醒已设置成功”或“状态已同步完成”。
- 如果写操作依赖具体任务 ID，而当前只有模糊任务名，先用项目数据或筛选结果列候选，再执行。
- 回复先自然说明结果；只有在列表较长或变更较多时，再补短结构。
- 多条任务的反馈优先按清单分组，再在每个清单下列任务。
