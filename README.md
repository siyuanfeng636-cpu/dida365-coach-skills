# Dida365 Coach Skills

结合滴答清单 MCP 的任务教练 skill 仓库，当前公开的主技能是 `dida-coach`。

它适合这些场景：

- 把长期目标拆成阶段计划
- 把具体任务安排成时间盒
- 做日复盘、周复盘和拖延模式分析
- 在延期、未完成和取消时给出闭环支持

## 一键安装

在已安装 Codex 的机器上运行：

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path superpowers/dida-coach
```

安装后重启 Codex，即可通过 `$dida-coach` 调用。

## MCP 依赖

需要先配置 `dida365` MCP：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

然后在客户端内执行 `/mcp` 完成授权。

## 示例请求

- `用 $dida-coach 帮我把“提高英语口语”拆成三个月计划`
- `用 $dida-coach 帮我把今天的报告排成 2 小时时间盒`
- `用 $dida-coach 复盘今天为什么效率差`
- `用 $dida-coach 把盒子 2 改到下午 2 点`

## 仓库结构

- [`superpowers/dida-coach/`](superpowers/dida-coach)：技能源码
- [`superpowers/dida-coach/SKILL.md`](superpowers/dida-coach/SKILL.md)：Codex skill 入口说明
- [`superpowers/dida-coach/README.md`](superpowers/dida-coach/README.md)：更详细的技能说明

## 版本

当前稳定版本：`v1.0.0`
