# 🎯 Dida-Coach: 你的 AI 任务教练 (Powered by Claude Code/MCP)

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

> **让滴答清单 (TickTick) 进化为主动式的 AI 教练。**  
> 不仅仅是记录，更是深度规划、专注执行与硬核复盘的完整闭环。

---

## 🤝 与 OpenClaw 的联动 (Powered by OpenClaw Skills)

Dida-Coach 不仅仅是一个独立的脚本，它是 **OpenClaw 生态系统** 中的核心技能。通过 OpenClaw，你可以实现以下深度联动：

*   **跨平台调用**：在任何支持 OpenClaw/Codex 的客户端中通过 `$dida-coach` 唤起。
*   **智能上下文共享**：Dida-Coach 可以感知 OpenClaw 当前的会话上下文，并根据你的项目背景自动优化任务拆解逻辑。
*   **技能组合连击**：你可以让 OpenClaw 先通过 `browser_agent` 调研某个技术点，然后直接调用 `dida-coach` 将调研结论转化为滴答清单中的执行时间盒。
*   **自动化安装与热更新**：支持 OpenClaw 标准的 `skill-installer` 协议，一键部署，自动同步最新功能。

---

## 🌟 核心亮点：为什么选择 Dida-Coach？

### 1. 🤖 四大教练人格，随心切换
拒绝冷冰冰的指令。你可以通过修改 `config.yaml` 或直接在对话中指定，选择最适合你的“督导”：
*   **温暖鼓励型 (Warm)**：在你低谷时给予动力。
*   **严格教练型 (Strict)**：铁腕治懒，专注产出。
*   **理性分析型 (Rational)**：数据驱动，逻辑严密。
*   **幽默调侃型 (Humorous)**：轻松有趣，化解压力。

### 2. 🧠 智能工作法推荐
不再纠结 25 分钟还是 50 分钟。系统根据任务难度、复杂度与你的精力状态，自动从 **经典番茄、长番茄、超昼夜节律 (90min)** 等多种模式中推荐最优方案。

### 3. 🛡️ MCP 原生语义安全
深度集成 Dida365 MCP 协议，通过自研的 `dida_semantics.py` 确保任务优先级 (`!1`/`!2`/`!3`) 映射精准，并特别解决了重复任务在 MCP 接口中的“假完成”状态判断问题。

### 4. 🔄 真正的闭环管理 (Closed-loop)
任务不是“建完就忘”。系统追踪 **创建 -> 执行 -> 检查点 -> 完成/延期/取消** 的完整状态机。每一步都有反馈，每一个失败都有归因分析。

### 5. 📊 深度拖延模式检测
复盘不只是看完成率。系统会识别你的“拖延模式”（例如：晚上 8 点后的任务总是失败？阅读类任务总是推迟？），并给出具体的自动化或拆解建议。

---

## 🛠️ 六大功能模块

| 模块 | 功能描述 |
| :--- | :--- |
| **🎯 目标深度拆解** | 将长期目标拆解为阶段性计划，最大 3 轮追问锁定背景，生成可交付里程碑。 |
| **📦 任务时间盒 (Time-Boxing)** | 将大块任务切分为具备明确产出 (Deliverable) 的时间片段。 |
| **🚩 检查点追踪 (Checkpoint)** | 在时间盒结束时自动介入，按 4 级完成度 (100%/80%/50%/未开始) 进行后续引导。 |
| **📅 动态排期优化** | 支持单盒子调整、批量顺延、时长扩展，并自动进行影响分析。 |
| **📝 日/周硬核复盘** | 生成结构化报告，包含峰值效率段、任务分布、拖延识别与改进策略。 |
| **🔍 失败归因分析** | 针对未完成任务，从难度、干扰、精力、时机等维度进行深度诊断。 |

---

## 🚀 配置与安装

### 1. 前置准备：MCP 授权
Dida-Coach 依赖 Dida365 MCP 服务器。首先在支持 MCP 的客户端（如 Claude Desktop 或 OpenClaw）中添加：
```bash
# 添加 MCP 节点
claude mcp add --transport http dida365 https://mcp.dida365.com
# 运行后在客户端内执行 /mcp 完成滴答清单的 OAuth 授权
```

### 2. 技能安装 (OpenClaw/Codex)
在终端运行 OpenClaw 官方安装脚本：
```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path superpowers/dida-coach
```

### 3. 个性化配置 (Optional)
你可以通过修改项目根目录下的 `config.yaml` 来深度定制你的教练：
*   **Persona**: 设置默认语气（warm/strict/rational/humorous）。
*   **Work Methods**: 调整番茄钟时长偏好。
*   **Reminders**: 配置任务开始前的提醒提前量。

---

## 📂 项目结构
```text
dida-coach/
├── skill.yaml          # OpenClaw 技能定义与触发器配置
├── SKILL.md            # 教练工作流入口说明
├── config.yaml         # 用户个性化偏好配置
├── prompts/            # 全场景 Prompt 模板 (系统/拆解/时间盒/复盘/闭环)
├── tools/              # 核心逻辑模块 (MCP 客户端/排程计算/复盘分析等)
├── agents/             # 代理配置与模型映射
├── references/         # 滴答清单字段语义参考文档
└── tests/              # 自动化测试用例
```

---

## 🏗️ 技术架构
*   **核心引擎**: Python 3.10+
*   **接入层**: OpenClaw Skill API / Codex
*   **存储与接口**: Dida365/TickTick via MCP (Model Context Protocol)
*   **智能模块**: 自研任务解析引擎 + 闭环状态机

---

## 🤝 贡献与反馈
欢迎提交 Issue 或 Pull Request 来完善这个“AI 教练”。如果你觉得有用，请点一个 **⭐ Star** 支持一下！

---
**Author**: [@siyuanfeng636-cpu](https://github.com/siyuanfeng636-cpu)  
**OpenClaw Ecosystem**: [Join our community](https://github.com/openclaw)  
**License**: MIT
