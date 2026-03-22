# 用 MCPorter 管理 Dida 接入 backend

如果你想解决“skill 只能提示配置，但不能稳定完成外部 MCP 接入与 OAuth”的问题，推荐默认走这条由 MCPorter 托管的本地 backend 路线。

## 它解决什么问题

这个 backend 只负责接入层，不做任务教练逻辑。它负责：

- 检查 dida365 是否已接入
- 把 dida365 写进 OpenClaw 的 `mcpServers`
- 返回 OpenClaw 半自动接入指引
- 生成滴答开放平台授权链接
- 监听本地 `http://localhost:38000/callback`
- 把本地 Open API token 写入 `~/.dida-coach/dida-openapi.env`

## 推荐注册方式

注册一个由 MCPorter 管理的 backend：

```bash
mcporter config add dida-auth-backend \
  --command "python3" \
  --arg "/ABSOLUTE/PATH/TO/scripts/dida_auth_backend.py"
```

如果你在仓库根目录，可以用：

```bash
mcporter config add dida-auth-backend \
  --command "python3" \
  --arg "/Users/fengsiyuan/docs/scripts/dida_auth_backend.py"
```

注册完以后，默认直接执行远程 MCP 授权：

```bash
mcporter auth https://mcp.dida365.com
```

预期流程是：

1. MCPorter 识别 dida365 远程 MCP
2. 浏览器打开滴答登录/授权页
3. 用户登录并点击授权
4. MCPorter 或客户端保存 token
5. 后续直接使用 dida365

## 常用 backend 动作

### 1. 查看状态

```bash
python3 scripts/dida_auth_backend.py status
```

### 2. 自动写入 OpenClaw dida365 MCP 配置

```bash
python3 scripts/dida_auth_backend.py configure-openclaw
```

### 3. 生成滴答开放平台授权链接

```bash
python3 scripts/dida_auth_backend.py authorization-url \
  --client-id YOUR_CLIENT_ID
```

### 4. 本地 OAuth + 自动落盘

```bash
python3 scripts/dida_auth_backend.py oauth-local \
  --client-id YOUR_CLIENT_ID \
  --client-secret YOUR_CLIENT_SECRET
```

### 5. JSONL 模式

如果 MCPorter 需要一个更容易适配的标准输入/输出循环，可以用：

```bash
python3 scripts/dida_auth_backend.py serve-jsonl
```

然后向 stdin 写入：

```json
{"action":"status"}
{"action":"configure-openclaw"}
{"action":"authorization-url","client_id":"YOUR_CLIENT_ID"}
```

## 和 dida-coach 的关系

- `dida-coach`：上层自然语言交互、时间盒、任务管理、复盘、生产力管控
- `dida-auth-backend`：底层接入/OAuth/配置/凭证状态

推荐让 `dida-coach` 默认调用这条 backend 路线，而不是直接让用户手工改配置文件或优先切到本地 Open API OAuth。
