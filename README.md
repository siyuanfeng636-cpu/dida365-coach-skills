# 🎯 Dida-Coach: 你的 AI 任务教练 (Powered by Claude Code/MCP)

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

> **让滴答清单 (TickTick) 进化为主动式的 AI 教练。**
> 不仅仅是记录，更是深度规划、专注执行与硬核复盘的完整闭环。

---

## 🌟 核心亮点：为什么选择 Dida-Coach？

### 1. 🤖 四大教练人格，随心切换
拒绝冷冰冰的指令。你可以根据当下的状态，选择最适合你的"督导"：
*   **温暖鼓励型 (Warm)**：在你低谷时给予动力。
*   **严格教练型 (Strict)**：铁腕治懒，专注产出。
*   **理性分析型 (Rational)**：数据驱动，逻辑严密。
*   **幽默调侃型 (Humorous)**：轻松有趣，化解压力。

### 2. 🧠 智能工作法推荐
不再纠结 25 分钟还是 50 分钟。系统根据任务难度、复杂度与你的精力状态，自动从 **经典番茄、长番茄、超昼夜节律 (90min)** 等多种模式中推荐最优方案。

### 3. 🛡️ MCP 原生语义安全
深度集成 Dida365 MCP 协议，通过自研的 `dida_semantics.py` 确保任务优先级 (`!1`/`!2`/`!3`) 映射精准，并特别解决了重复任务在 MCP 接口中的"假完成"状态判断问题。

### 4. 🔄 真正的闭环管理 (Closed-loop)
任务不是"建完就忘"。系统追踪 **创建 -> 执行 -> 检查点 -> 完成/延期/取消** 的完整状态机。每一步都有反馈，每一个失败都有归因分析。

### 5. 📊 深度拖延模式检测
复盘不只是看完成率。系统会识别你的"拖延模式"（例如：晚上 8 点后的任务总是失败？阅读类任务总是推迟？），并给出具体的自动化或拆解建议。

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

## 🚀 快速上手

### 1. 前置准备
确保已配置 `dida365` MCP 服务器：
```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

### 2. 一键安装
在已安装 Codex/Claude Code 的终端运行：
```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path superpowers/dida-coach
```

### 3. 开始对话
*   "用 `$dida-coach` 帮我把'学习 React 框架'拆成 21 天计划"
*   "用 `$dida-coach` 帮我把下午的调研任务排成 3 小时时间盒"
*   "用 `$dida-coach` 复盘一下这周为什么核心指标没达成"

---

## 🏗️ 技术架构
*   **核心引擎**: Python 3.10+
*   **接入层**: Codex/Claude Code Skill API
*   **存储与接口**: Dida365/TickTick via MCP (Model Context Protocol)
*   **组件**: 配置管理器、任务解析器、时间盒计算引擎、复盘分析仪

---

## 📂 项目结构

```
dida-coach/
├── README.md          # 本文件
├── SKILL.md           # Codex skill 入口说明
├── skill.yaml         # Claude Code 风格 skill 定义
├── config.yaml        # 默认文风、工作法、提醒和闭环配置
├── prompts/           # 各场景 prompt 模板
├── tools/             # 解析、排程、配置和复盘分析工具
├── agents/            # Agent 配置
├── references/        # 参考资料
└── tests/             # 测试用例
```

---

## 🤝 贡献与反馈
欢迎提交 Issue 或 Pull Request 来完善这个"AI 教练"。如果你觉得有用，请点一个 **⭐ Star** 支持一下！

---
**Author**: [@siyuanfeng636-cpu](https://github.com/siyuanfeng636-cpu)
**License**: MIT
