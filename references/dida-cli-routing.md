# dida-cli 命令路由

这份路由表是 `dida-coach` 的唯一执行基线。

所有滴答读写都优先用 `dida-cli`，不要再发明远程 MCP 工具名。

## 认证

- 登录：`dida auth login`
- 查看状态：`dida auth status`
- 登出：`dida auth logout`

## 清单

- 列出所有清单：`dida project list --json`
- 按 ID 获取清单：`dida project get <projectId> --json`
- 获取清单及其中任务：`dida project data <projectId> --json`
- 创建清单：`dida project create --name "<name>" --json`
- 更新清单：`dida project update <projectId> --name "<name>" --json`

项目选择规则：

- 先用 `dida project list --json` 找 `name`
- 如果同名清单不止一个，必须让用户确认
- 不要猜测清单 ID

## 任务

- 获取任务：`dida task get <projectId> <taskId> --json`
- 创建任务：`dida task create --title "<title>" --project <projectId> --json`
- 更新任务：`dida task update <taskId> --id <taskId> --project <projectId> ... --json`
- 完成任务：`dida task complete <projectId> <taskId>`
- 删除任务：`dida task delete <projectId> <taskId>`
- 移动任务：`dida task move --from <sourceProjectId> --to <destProjectId> --task <taskId>`
- 筛选任务：`dida task filter --projects <ids> --start-date <iso> --end-date <iso> --status <codes> --json`
- 查询已完成任务：`dida task completed --projects <ids> --start-date <iso> --end-date <iso> --json`

## 推荐路由

- “列出所有清单”
  - `dida project list --json`

- “查看某个清单及其任务”
  - 先 `dida project list --json` 找 `projectId`
  - 再 `dida project data <projectId> --json`

- “创建一个任务”
  - 先 `dida project list --json` 找目标清单
  - 再 `dida task create --title ... --project <projectId> --json`
  - 创建后用 `dida task get <projectId> <taskId> --json` 回读

- “更新标题 / 提醒 / 截止时间 / 优先级”
  - 先拿到 `projectId` + `taskId`
  - 再 `dida task update <taskId> --id <taskId> --project <projectId> ... --json`
  - 更新后立刻 `dida task get <projectId> <taskId> --json`

- “标记完成”
  - `dida task complete <projectId> <taskId>`
  - 完成后立刻 `dida task get <projectId> <taskId> --json`

- “移动到其他清单”
  - `dida task move --from <sourceProjectId> --to <destProjectId> --task <taskId>`
  - 移动后用目标清单的 `dida project data <projectId> --json` 或 `dida task get ... --json` 校验

- “今天有哪些任务 / 本周有哪些任务”
  - 先 `dida project list --json` 收集项目 ID
  - 再 `dida task filter --projects <allProjectIds> --start-date <iso> --end-date <iso> --status 0 --json`
  - 如果还要看已完成，再补 `dida task completed --projects <allProjectIds> --start-date <iso> --end-date <iso> --json`

- “按优先级筛今天未完成任务”
  - `dida task filter --projects <allProjectIds> --start-date <iso> --end-date <iso> --status 0 --priority 1,3,5 --json`

## 字段约束

- 优先级使用 dida 数值：`0=无`、`1=低`、`3=中`、`5=高`
- 时间统一传 ISO 8601，并带上 `--time-zone Asia/Shanghai` 或当前用户时区
- 提醒走 `--reminders`
- 创建/更新后必须回读，不要只汇报“已成功”

## 安全约束

- 删除任务属于破坏性操作，必须明确确认
- 清单/任务同名或范围模糊时，必须先澄清
- 没拿到 `projectId` / `taskId` 前，不要假装已经定位到正确任务
