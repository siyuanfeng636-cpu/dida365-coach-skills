# 滴答清单 MCP 工具路由

这份路由表用于约束 `dida-coach` 在调用滴答清单 MCP 时，优先使用哪些真实工具名。

不要自行发明类似 `get_today_tasks`、`create_timebox_task`、`list_all_tasks` 之类不存在的工具名。

## 查询任务

- 按关键词搜索任务：`search_task`
- 按任务 ID 读取完整内容：`get_task_by_id`
- 查询今天或相对时间范围内的未完成任务：`list_undone_tasks_by_time_query`
  - 支持：`today`、`last24hour`、`last7day`、`tomorrow`、`next24hour`
- 查询指定日期范围内的未完成任务：`list_undone_tasks_by_date`
- 查询指定清单中、指定日期范围内的已完成任务：`list_completed_tasks_by_date`
- 多条件组合筛选任务：`filter_tasks`

## 查询清单

- 列出所有清单：`list_projects`
- 按清单 ID 获取详情：`get_project_by_id`
- 获取清单详情并带出其中未完成任务：`get_project_with_undone_tasks`
- 在某个清单里查找特定任务：`get_task_in_project`

## 管理任务

- 创建单个任务：`create_task`
- 批量创建任务：`batch_add_tasks`
- 完成单个任务：`complete_task`
- 批量完成某清单中的多个任务：`complete_tasks_in_project`
  - 单次最多 20 个
- 更新任务属性：`update_task`
- 移动任务到其他清单：`move_task`
- 批量更新任务属性：`batch_update_tasks`

## 推荐路由

- “我今天有哪些任务？”
  - 优先：`list_undone_tasks_by_time_query(today)`
  - 如果用户还要看今天完成了什么，再补：`list_completed_tasks_by_date`

- “帮我创建一个任务”
  - 使用：`create_task`
  - 创建后立刻：`get_task_by_id`

- “把这个任务标记完成”
  - 单个任务：`complete_task`
  - 清单里一批任务：`complete_tasks_in_project`

- “把任务改到下午 3 点 / 改优先级 / 改提醒”
  - 使用：`update_task`
  - 更新后立刻：`get_task_by_id`

- “把任务移到另一个清单”
  - 使用：`move_task`
  - 移动后可用：`get_task_by_id` 或 `get_task_in_project` 校验

- “按清单看今天还没做完的”
  - 优先：`get_project_with_undone_tasks`
  - 如果还要加优先级、标签、状态等条件：`filter_tasks`

- 日复盘 / 周复盘
  - 未完成任务：`list_undone_tasks_by_time_query` 或 `list_undone_tasks_by_date`
  - 已完成任务：`list_completed_tasks_by_date`
  - 不要只看未完成任务就做完成率统计

## 回读校验要求

凡是创建、更新、移动、完成之后，都要至少回读一次，优先用：

- `get_task_by_id`
- 或与场景匹配的清单级查询工具

必须校验这些字段是否真的落盘：

1. 标题
2. 优先级
3. 截止时间
4. 提醒时间
5. 当前完成状态
