# Dida-Coach：滴答清单 AI 任务教练

[![Stars](https://img.shields.io/github/stars/siyuanfeng636-cpu/dida365-coach-skills?style=social)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-v1.4.0-blue.svg)](https://github.com/siyuanfeng636-cpu/dida365-coach-skills/releases)

> 让滴答清单成为你的 AI 效率教练。
> 这版技能只使用 `dida-cli`，不再依赖远程 MCP。

## 核心能力

- 目标拆解：把长期目标拆成阶段任务和检查点
- 时间盒：按时段落地成真实滴答任务，并带提醒
- 通用任务管理：查清单、查任务、创建、更新、完成、移动
- 生产力管控：本地沉淀 dashboard、承诺、等待项、专注记录、周月复盘
- 闭环跟进：任务延期、变更、提醒前先回读当前状态

## 接入方式

默认自动认证：`dida-cli`

只支持 `dida-cli`：

```bash
npm install -g @suibiji/dida-cli
dida auth login
dida auth status
```

浏览器授权完成后，就可以直接使用 `$dida-coach`。

## 真实 CLI 基线

这版 skill 的滴答执行层统一基于这些命令：

- 登录：`dida auth login`
- 查看状态：`dida auth status`
- 列清单：`dida project list --json`
- 查清单详情：`dida project get <projectId> --json`
- 查清单及其任务：`dida project data <projectId> --json`
- 创建任务：`dida task create ... --json`
- 获取任务：`dida task get <projectId> <taskId> --json`
- 更新任务：`dida task update <taskId> --id <taskId> --project <projectId> ... --json`
- 完成任务：`dida task complete <projectId> <taskId>`
- 移动任务：`dida task move --from <sourceProjectId> --to <destProjectId> --task <taskId>`
- 筛选任务：`dida task filter ... --json`
- 查询已完成：`dida task completed ... --json`

完整路由见：

- [references/dida-cli-routing.md](/Users/fengsiyuan/docs/references/dida-cli-routing.md)

## 快速上手

1. 安装技能

```bash
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo siyuanfeng636-cpu/dida365-coach-skills \
  --path .
```

2. 安装并登录 dida-cli

```bash
npm install -g @suibiji/dida-cli
dida auth login
dida auth status
```

3. 开始使用

```text
$dida-coach 列出所有清单
$dida-coach 帮我创建一个今天下午 3 点截止、提前 30 分钟提醒的任务，放到工作清单
$dida-coach 把“买牛奶”移到生活清单
$dida-coach 帮我把今天的报告排成 2 小时时间盒
$dida-coach 复盘今天
$dida-coach 帮我建立生产力系统
```

## 本地生产力系统

初始化后会写入：

- `~/.dida-coach/productivity/dashboard.md`
- `~/.dida-coach/productivity/commitments/`
- `~/.dida-coach/productivity/planning/`
- `~/.dida-coach/productivity/reviews/`
- `~/.dida-coach/productivity/focus/`
- `~/.dida-coach/productivity/routines/`

这层不是第二套任务数据库，只保存管理所需的摘要和索引。

## 关键行为约束

- 任务反馈、提醒和复盘中的具体任务，默认带上所属清单名称
- 到期提醒、延期提醒、变更后提醒，都会先回读滴答当前任务
- 如果时间、内容或状态有变化，会先通报最新版本，再决定是否继续提醒
- 创建或更新后必须回读，不会只报“已成功”
- 所有相对时间判断都以用户当前本地时区为准

## 时区与性能说明

- 所有“现在 / 今天 / 明天 / 还有多久 / 下午几点前”这类相对时间判断，都以用户当前本地时区为准
- 说“还有 X 分钟 / 小时”前，必须基于当前本地时间和目标绝对时间重新计算
- 任务反馈、提醒和复盘里的具体任务，默认都会带上所属清单名称；多任务场景优先按清单分组反馈
- 这版 skill 以本地 CLI 为主，通常比远程 MCP 链路更直接；但写操作仍会保留必要回读，所以批量动作会更慢一些

## 仓库结构

- [SKILL.md](/Users/fengsiyuan/docs/SKILL.md)：技能入口说明
- [skill.yaml](/Users/fengsiyuan/docs/skill.yaml)：技能元数据与触发规则
- [prompts/](/Users/fengsiyuan/docs/prompts)：对话流程
- [tools/dida_cli_auth.py](/Users/fengsiyuan/docs/tools/dida_cli_auth.py)：CLI 安装/登录/状态辅助
- [references/dida-cli-routing.md](/Users/fengsiyuan/docs/references/dida-cli-routing.md)：CLI 路由基线

## 版本

当前稳定版本：`v1.4.0`
