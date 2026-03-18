# Dida Coach

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.0.1-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

把滴答清单变成一个可执行的 AI 任务教练。这个 skill 负责目标拆解、时间盒安排、复盘分析和延期后的闭环跟进。

## 核心能力

- 长期目标拆解成阶段计划和可执行任务
- 单次任务拆成带成果定义的时间盒
- 日复盘、周复盘和拖延模式分析
- 延期、改时间、未完成后的闭环追踪
- 基于滴答字段语义做优先级、提醒和完成状态校验

## 一键安装

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path .
```

安装后重启 Codex、OpenClaw 或兼容客户端，即可通过 `$dida-coach` 调用。

## MCP 接入

滴答清单 MCP 服务地址是：

- `https://mcp.dida365.com`

为了尽量降低上手门槛，当前文档采用“浏览器授权优先”：

- 如果页面里已经有 `Connect`、`Authorize`、`Sign in`、`Enable` 之类按钮，直接点击并在浏览器完成 OAuth。
- 只有当客户端不能自动注册 MCP 时，才手动添加 `dida365`。

不同客户端的最短接入路径见：

- [`references/mcp-client-setup.md`](references/mcp-client-setup.md)

Claude Code 的兜底命令仍然保留：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

## 常见使用方式

- `用 $dida-coach 帮我把“提高英语口语”拆成三个月计划`
- `用 $dida-coach 帮我把今天的报告排成 2 小时时间盒`
- `用 $dida-coach 复盘今天为什么效率差`
- `用 $dida-coach 把盒子 2 改到下午 2 点`

## 仓库结构

- [`SKILL.md`](SKILL.md)：技能入口说明
- [`skill.yaml`](skill.yaml)：技能元数据与触发器
- [`config.yaml`](config.yaml)：默认人格、工作法和提醒配置
- [`prompts/`](prompts/)：各场景 prompt
- [`tools/`](tools/)：MCP 检测、解析、排程和复盘逻辑
- [`references/`](references/)：滴答字段语义与客户端接入速查
- [`tests/`](tests/)：回归测试

## 版本

当前稳定版本：`v1.0.1`
