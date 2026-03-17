# Dida Coach

结合滴答清单 MCP 的任务教练 skill，负责：

- 把长期目标拆成阶段计划和可执行任务
- 把单次任务排成时间盒并设置检查点
- 做日复盘、周复盘和拖延模式分析
- 在延期、未完成和取消时提供闭环支持

## 目录

- `skill.yaml`: 兼容 Claude Code 风格的 skill 入口定义
- `SKILL.md`: 兼容 Codex skill 体系的使用说明
- `config.yaml`: 默认文风、工作法、提醒和闭环配置
- `prompts/`: 各场景 prompt 模板
- `tools/`: 解析、排程、配置和复盘分析工具

## MCP 依赖

需要本地配置 `dida365` MCP：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

然后在客户端内执行 `/mcp` 完成授权。

## 典型用法

- “我想提高英语口语”
- “帮我把今天的报告拆成 2 小时时间盒”
- “复盘今天为什么效率差”
- “把盒子 2 改到下午 2 点”
