# Dida-Coach：滴答清单 AI 任务教练

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.0.3-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

> **让滴答清单成为你的 AI 效率教练。**
> 不只是待办清单——而是一套覆盖深度规划、专注执行、数据复盘的全周期效率系统。

```
"$dida-coach 帮我把'提高英语口语'拆成 3 个月计划"
```

---

## 为什么选择 Dida-Coach？

大多数 AI 效率工具止步于*创建*任务。Dida-Coach 更进一步：它能**规划**、**排程**、**追踪**、**复盘**，并从你的执行数据中**学习**——全程通过自然对话完成。

| 痛点 | Dida-Coach 的解决方案 |
| :--- | :--- |
| AI 方案停在聊天窗口，永远到不了手机上 | 通过 MCP 协议同步至滴答清单——手机、平板、手表随时可用 |
| 通用番茄钟无视任务上下文 | 智能工作方法引擎根据任务类型与精力状态推荐 25 / 30 / 50 / 90 分钟时段 |
| 错过截止日期后无人跟进 | 闭环状态机：创建 → 执行 → 检查点 → 完成 / 重排 / 取消 |
| 复盘只是模糊的"今天感觉如何？" | 模式识别可定位*何时*、*为何*拖延，并给出自动化建议 |

---

## 核心功能

### 1. 目标拆解

将长期目标拆分为阶段性计划与可衡量的里程碑。最多 3 轮上下文提问，确保计划贴合你的实际情况。

```
$dida-coach 帮我把"系统学习 Rust"拆成两个月计划
```

### 2. 智能 Time-Boxing（时间盒）

每个时间盒包含一个**可验证的交付物**——而非仅仅是一段时长。引擎自动推荐最佳工作方法：

| 方法 | 专注时长 | 适用场景 |
| :--- | :--- | :--- |
| 经典番茄钟 | 25 分钟 | 快速任务、邮件批处理 |
| 弹性番茄钟 | 30 分钟 | 通用知识工作 |
| 长番茄钟 | 50 分钟 | 深度写作、编程 |
| 超日节律 (Ultradian Rhythm) | 90 分钟 | 创意工作、复杂分析 |

### 3. 全面任务管理（v1.0.3 新增）

不止于教练——通过自然语言管理你的整个滴答清单工作流：

- **查询**："今天有哪些任务？" / "显示所有清单"
- **创建**："创建一个任务：买菜，明天下午 6 点截止，高优先级"
- **更新**："把提醒改成提前 30 分钟"
- **完成**："把报告任务标记为已完成"
- **移动**："把'买牛奶'移到生活清单"
- **筛选**："按优先级筛选今天未完成的任务"

每次写入操作均遵循**写入-读取-验证**协议——教练会从滴答清单回读数据，确认字段已正确持久化。

### 4. 多客户端 MCP 支持（v1.0.3 新增）

一套技能，多端通用。为每个平台提供详细的配置指南：

| 客户端 | 配置方式 |
| :--- | :--- |
| Claude Desktop | Connectors 界面 → 一键 OAuth 授权 |
| ChatGPT | 开发者模式 → 自定义应用 |
| Claude Code | `claude mcp add` 命令行 |
| Cursor | `.cursor/mcp.json` 配置文件 |
| VS Code | 命令面板或 `.vscode/mcp.json` |
| OpenClaw / ClawHub | 内置 MCP 面板 |

> **浏览器优先授权**：如果客户端显示"连接"按钮，直接点击即可。手动配置仅作为备用方案。

### 5. MCP 工具路由（v1.0.3 新增）

严格的路由表将每一种用户意图映射到*真实的*滴答清单 MCP 工具名——杜绝幻觉式 API 调用。

```
"今天有什么任务？"  →  list_undone_tasks_by_time_query
"创建一个任务"      →  create_task → get_task_by_id（验证）
"移到工作清单"      →  move_task → get_task_by_id（验证）
"周复盘"            →  list_completed_tasks_by_date + list_undone_tasks_by_date
```

### 6. 四种教练人格

选择最能激励你的风格——可在 `config.yaml` 中配置，也可在对话中随时切换：

| 人格 | 风格 |
| :--- | :--- |
| **温暖鼓励型** | 在精力低迷时给予温柔支持 |
| **严格教练型** | 零废话，以结果为导向的问责 |
| **理性分析型** | 数据驱动，逻辑清晰，注重模式发现 |
| **幽默风趣型** | 减轻压力，让复盘也变得有趣 |

### 7. 深度复盘与拖延检测

每日和每周复盘不仅看完成率：

- 峰值效率时间窗口分析
- 任务类型分布统计
- 拖延模式识别（例如："晚上 8 点后的阅读任务总是失败"）
- 自动化候选项识别
- 具体可行的改进建议

### 8. 闭环状态机

每个任务全生命周期追踪：

```
已创建 → 执行中 → 检查点 → 已完成
                      ↓
                   已重排 → 执行中 → ...
                      ↓
                   已取消（附原因）
```

错过的任务会先进行**根因分析**（难度过高？注意力分散？时段不对？），再决定重排方案——而非简单地"明天再试"。

---

## 快速上手

### 1. 连接滴答清单 MCP

```bash
# Claude Code
claude mcp add --transport http dida365 https://mcp.dida365.com

# 然后在会话中授权
/mcp
```

其他客户端请参阅 [`references/mcp-client-setup.md`](references/mcp-client-setup.md)。

### 2. 安装技能

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path .
```

### 3. 开始使用

```bash
$dida-coach 帮我把今天的报告排成 2 小时时间盒
$dida-coach 告诉我今天有哪些未完成任务
$dida-coach 列出所有清单并把"买牛奶"移到生活清单
$dida-coach 复盘今天为什么效率差
$dida-coach 把盒子 2 改到下午 2 点
```

### 4. 个性化配置（可选）

编辑 `config.yaml` 以设置默认人格、偏好工作方法和提醒时间表。

---

## 架构："AI 思考，滴答执行"

```
┌─────────────────────┐     MCP 协议       ┌──────────────────┐
│  OpenClaw / Claude   │◄───────────────────►│   滴答清单云端   │
│  （规划大脑）         │   读取 / 写入任务   │  （执行中枢）     │
└─────────┬───────────┘                      └────────┬─────────┘
          │                                           │
    深度推理                                     多设备同步
    目标拆解                                     手机 / 平板 / 手表
    工作方法匹配                                 推送通知
    复盘分析                                     一键完成
```

**桌面端规划。移动端执行。数据回流。AI 持续学习。**

---

## 项目结构

```
dida-coach/
├── skill.yaml              # 技能元数据、触发器、入口点
├── SKILL.md                # 工作流入口 & 意图路由指南
├── config.yaml             # 人格、工作方法、提醒配置
├── prompts/
│   ├── system.md           # 核心系统角色 & MCP 路由
│   ├── task_breakdown.md   # 目标拆解流程
│   ├── task_management.md  # 通用 CRUD 任务操作（新增）
│   ├── timebox_creation.md # 时间盒排程流程
│   ├── checkpoint.md       # 检查点跟进
│   ├── rescheduling.md     # 时间调整流程
│   ├── daily_review.md     # 每日复盘
│   ├── weekly_review.md    # 每周复盘
│   ├── closure.md          # 收尾 & 后续跟进
│   ├── setup.md            # 首次 MCP 配置
│   └── coach_personas/     # 4 种人格定义
├── tools/
│   ├── mcp_client.py       # MCP 检测 & 配置引导
│   ├── config_manager.py   # 配置加载 & 用户覆盖
│   ├── task_parser.py      # 目标与时间盒的自然语言解析
│   ├── timebox_calculator.py  # 排程计算
│   ├── work_method_recommender.py  # 智能工作方法推荐
│   ├── review_analyzer.py  # 完成情况分析 & 报告
│   └── dida_semantics.py   # 优先级映射 & 状态安全
├── references/
│   ├── dida-field-semantics.md   # 滴答清单字段参考
│   ├── mcp-client-setup.md       # 多客户端配置指南（新增）
│   └── mcp-tool-routing.md       # 意图 → MCP 工具映射（新增）
├── agents/                 # Agent 配置
├── assets/                 # UI 原型
└── tests/                  # 回归测试
```

---

## 技术栈

- **引擎**：Python 3.10+
- **接口**：OpenClaw Skill API / Codex
- **后端**：滴答清单 via MCP（Model Context Protocol）
- **智能层**：自定义 NLP 解析器 + 闭环状态机

---

## v1.0.3 更新内容

- **通用任务管理**：完整 CRUD 支持——通过自然对话查询、创建、更新、完成、移动、筛选任务
- **MCP 工具路由**：严格的意图-工具映射，杜绝幻觉式 API 调用
- **多客户端配置**：涵盖 6 个平台的分步指南（Claude Desktop、ChatGPT、Claude Code、Cursor、VS Code、OpenClaw）
- **浏览器优先授权**：OAuth 流程优先使用一键浏览器授权，手动 CLI 配置仅作备用
- **写入-读取-验证协议**：每次写入操作均从滴答清单回读，确认字段持久化
- **扩展触发器**：更丰富的任务管理命令意图匹配
- **自然对话**：系统提示词全面重写，更少表单填写，更多自然教练式对话

---

## 参与贡献

欢迎提交 Issue 和 PR。如果觉得有用，点个 **Star** 帮助更多人发现这个项目。

---

**作者**：[@siyuanfeng636-cpu](https://github.com/siyuanfeng636-cpu)
**OpenClaw 生态**：[github.com/openclaw](https://github.com/openclaw)
**协议**：MIT
