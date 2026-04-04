# 滴答 CLI 设置引导

检测到你还没有连上滴答，请按下面步骤完成配置。

这版 skill 只认 `dida-cli`，不再引导远程 MCP、OpenClaw、MCPorter 或本地 OpenAPI OAuth。

## 第一步：检查 dida-cli

先检查本机是否已有 `dida`：

```bash
dida --version
```

如果没有，再安装：

```bash
npm install -g @suibiji/dida-cli
```

## 第二步：执行登录

执行：

```bash
dida auth login
```

浏览器会打开滴答登录/授权页。用户完成登录和授权后回到终端。

## 第三步：确认状态

执行：

```bash
dida auth status
```

如果状态正常，再继续后续任务管理、时间盒、复盘和生产力管控。

## 常见问题

Q: 浏览器没有打开怎么办？
A: 先确认 `dida auth login` 命令是否正常启动，再检查默认浏览器、弹窗拦截或网络。

Q: 登录后还是不行怎么办？
A: 先执行 `dida auth status` 看是否真的保存了 token；如果没有，再重新执行 `dida auth login`。

Q: 能不能继续走远程 MCP？
A: 这版 skill 默认不考虑远程 MCP。接入、认证和执行都统一走 `dida-cli`。

Q: 完成登录后下一步是什么？
A: 告诉我“已登录”或直接说你的任务，例如“列出所有清单”“帮我创建一个任务”“复盘今天”。
