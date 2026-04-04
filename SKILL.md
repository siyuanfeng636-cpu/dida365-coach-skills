---
name: dida-coach
description: 基于 dida-cli 和本地生产力系统的任务教练技能，用于把目标拆解成阶段计划、把任务转换成时间盒，并自然地查询、创建、更新、完成、移动任务，支持管理视角、承诺跟踪、周/月复盘与闭环跟进。用户提到“拆目标”“做计划”“时间盒”“复盘”“改时间”“提醒”“拖延”“查任务”“完成任务”“清单管理”“生产力系统”“承诺”“等待项”时使用。
---

# Dida Coach

将 `dida-cli` 当作滴答执行层，把本地生产力系统当作管控层，再把更自然的教练式对话、时间盒调度、通用任务管理、复盘分析和闭环跟进组合成一个工作流。

## 使用顺序

1. 先读取 [`tools/dida_cli_auth.py`](./tools/dida_cli_auth.py)，检查 `dida` 是否已安装，并确认当前登录状态。
2. 如果是首次接入或登录失效，读取 [`references/dida-cli-auth-setup.md`](./references/dida-cli-auth-setup.md)，优先走 `dida auth login`。
3. 再读取 [`tools/config_manager.py`](./tools/config_manager.py)，加载用户文风、工作法和提醒偏好。
4. 涉及滴答读写时，先读取 [`references/dida-cli-routing.md`](./references/dida-cli-routing.md) 确认真实 CLI 命令，再读取 [`references/dida-field-semantics.md`](./references/dida-field-semantics.md)。
5. 按用户意图选择对应 prompt：
   - 首次配置或登录问题：[`prompts/setup.md`](./prompts/setup.md)
   - 目标拆解：[`prompts/task_breakdown.md`](./prompts/task_breakdown.md)
   - 通用任务管理：[`prompts/task_management.md`](./prompts/task_management.md)
   - 生产力管控：[`prompts/productivity_management.md`](./prompts/productivity_management.md)
   - 时间盒安排：[`prompts/timebox_creation.md`](./prompts/timebox_creation.md)
   - 检查点跟进：[`prompts/checkpoint.md`](./prompts/checkpoint.md)
   - 改时间：[`prompts/rescheduling.md`](./prompts/rescheduling.md)
   - 日复盘：[`prompts/daily_review.md`](./prompts/daily_review.md)
   - 周复盘：[`prompts/weekly_review.md`](./prompts/weekly_review.md)
   - 月复盘：[`prompts/monthly_review.md`](./prompts/monthly_review.md)
   - 闭环追踪：[`prompts/closure.md`](./prompts/closure.md)
6. 需要结构化判断时，使用 `tools/` 下的工具模块；需要具体对话话术时，再读取相应 prompt 和文风文件。

## 工具选择

- `tools/dida_cli_auth.py`
  用于检测 dida CLI、生成安装/登录/状态命令，并返回自动认证说明。
- `references/dida-cli-auth-setup.md`
  用于指导 `npm install -g @suibiji/dida-cli`、`dida auth login`、`dida auth status`。
- `references/dida-cli-routing.md`
  用于把“查任务 / 查清单 / 创建 / 更新 / 完成 / 移动 / 复盘”映射到真实存在的 dida-cli 命令。
- `tools/config_manager.py`
  用于加载默认配置和用户覆盖配置，并读取文风/工作法/提醒设置。
- `tools/productivity_system.py`
  用于管理 `~/.dida-coach/productivity/`，负责初始化本地生产力系统、生成 dashboard/承诺/专注/周月复盘摘要，并维护受管文件。
- `tools/task_parser.py`
  用于从自然语言中提取目标类型、任务描述、优先级、标签和改时间参数。
- `tools/dida_semantics.py`
  用于统一滴答优先级映射，并保守判定“当前任务是否真的完成”。
- `tools/timebox_calculator.py`
  用于计算时间盒、调整排程、生成检查点和人类可读时间表。
- `tools/work_method_recommender.py`
  用于根据任务特征推荐番茄/长番茄/超昼夜节律等工作法。
- `tools/review_analyzer.py`
  用于分析任务完成率、未完成模式和自动化机会，并生成日/周复盘文本。

## 关键约束

- 未登录 dida-cli 时，不假装已经写入滴答清单；先明确提示安装和登录步骤。
- 默认接入只有一条：`npm install -g @suibiji/dida-cli` -> `dida auth login` -> `dida auth status`。
- 所有滴答读写都优先使用 dida-cli；不要再使用远程 MCP、OpenClaw 接入、MCPorter、OpenAPI OAuth 作为当前技能主路径。
- 任何任务读写、查询、移动、完成、复盘基线都以 [`references/dida-cli-routing.md`](./references/dida-cli-routing.md) 为准，不要发明不存在的 CLI 子命令。
- 单个明确写操作默认直接执行并回读；高风险批量动作再确认。
- 缺信息时先推断再补问，不要把用户带进表单式追问。
- 对查询类请求可以直接读取并汇总；对创建、更新、完成、移动这类写操作，仍然要先说明动作，再执行并回读。
- 对任何到期提醒、检查点提醒、延期提醒或变更后提醒，都必须先读取滴答当前任务，再决定是否提醒；如果任务已经变更，先通报最新时间和内容。
- 任务反馈、执行结果、提醒和复盘举例时，都要带上所属清单名称；如果有多条任务，优先按清单分组汇报。
- 所有“今天 / 明天 / 现在 / 还有多久 / 下午几点前”这类相对时间判断，都必须以用户当前本地时区为准；如果当前时间来源不可靠，优先汇报绝对时间，不要口算剩余时长。
- 涉及截止时间、提醒时间和检查点倒计时时，先把“当前本地时间”和“目标绝对时间”写清，再计算分钟/小时差。
- 每个时间盒都要包含可验证的成果定义，而不是只有时长。
- 用户未完成任务时，先判断阻碍，再给补救方案，不要只做情绪化鼓励。
- 文风由 `config.yaml` 决定；如用户临时指定更严厉或更温和的风格，允许按本次对话覆盖。
- 创建或更新滴答任务后，必须回读校验优先级、截止时间、提醒时间和当前状态。
- 本地生产力系统固定写入 `~/.dida-coach/productivity/`；首次初始化前必须明确告知并拿到确认。
- 本地层只保存 dashboard、承诺、等待项、专注、例行、周月复盘和摘要索引，不复制完整滴答任务库。
