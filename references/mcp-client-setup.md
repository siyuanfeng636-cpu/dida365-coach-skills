# 滴答清单 MCP 客户端接入速查

滴答清单 MCP 服务地址：

- `https://mcp.dida365.com`

优先原则：

1. 如果当前客户端已经出现 `Connect`、`Authorize`、`Sign in`、`Enable` 之类按钮，直接点按钮。
2. 只有当客户端不能自动注册 MCP 时，才手动补配置。

## Claude Desktop

1. 打开 `Customize > Connectors`
2. 点击 `+`，选择 `Add Connector`
3. 填入 `https://mcp.dida365.com`
4. 点击 `Connect`，在浏览器完成 OAuth 授权

## ChatGPT

1. 打开 `设置 > 应用 > 高级设置`
2. 开启 `开发人员模式`
3. 点击 `创建应用`
4. 填入 `https://mcp.dida365.com`
5. 保存后按页面提示完成 OAuth 授权

## Claude Code

1. 运行：

```bash
claude mcp add --transport http dida365 https://mcp.dida365.com
```

2. 在会话中运行 `/mcp`
3. 按提示打开浏览器并完成 OAuth 授权

## Cursor

1. 打开 `Cursor Settings`
2. 进入 `Tools & MCP`
3. 点击 `Add Custom MCP`
4. 在 `.cursor/mcp.json` 中添加：

```json
{
  "mcpServers": {
    "dida365": {
      "url": "https://mcp.dida365.com"
    }
  }
}
```

5. 保存后重新打开 `Tools & MCP`
6. 找到 `dida365`，点击 `connect`
7. 在浏览器完成 OAuth 授权

## VS Code

方式一：命令面板添加

1. 打开命令面板
2. 运行 `Add Server`
3. 选择 `HTTP (HTTP or Server-Sent Events)`
4. 输入 `https://mcp.dida365.com`
5. 输入服务 ID：`dida365`
6. 选择作用范围：工作区或全局
7. 按提示完成浏览器授权

方式二：手动配置 `.vscode/mcp.json`

```json
{
  "servers": {
    "dida365": {
      "type": "http",
      "url": "https://mcp.dida365.com"
    }
  }
}
```

保存后根据提示完成浏览器授权。

## OpenClaw / ClawHub / 其他兼容客户端

1. 先找页面中的 `dida365` 连接按钮或 MCP 依赖面板
2. 如果能直接点 `Connect` 或 `Authorize`，优先走浏览器授权
3. 如果页面不支持自动注册，再按客户端的 MCP 设置页手动添加：
   - 服务名：`dida365`
   - URL：`https://mcp.dida365.com`
   - 传输方式：`HTTP` 或 `streamable_http`
