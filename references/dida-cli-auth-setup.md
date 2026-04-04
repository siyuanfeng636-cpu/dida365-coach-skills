# 使用 dida-cli 自动认证滴答

如果你想优先走“本地命令行自动拉起浏览器登录”的方式，可以使用 `dida-cli`。

对应的 ClawHub skill 说明是：

- 安装：`npm install -g @suibiji/dida-cli`
- 登录：`dida auth login`
- 状态检查：`dida auth status`

## 推荐流程

1. 先检查本机是否已安装 `dida`
2. 如果没安装，执行：

```bash
npm install -g @suibiji/dida-cli
```

3. 然后执行：

```bash
dida auth login
```

4. 浏览器会打开滴答登录/授权页，完成授权后回到终端
5. 再执行：

```bash
dida auth status
```

## 适用范围

- 适合希望“由 Agent 直接执行命令并拉起浏览器完成 OAuth PKCE”的场景
- 适合本地 CLI 驱动的滴答能力

## 边界

- 这条路完成的是 `dida-cli` 自己的本地认证
- 登录成功后，后续查询、创建、更新、完成、移动任务都继续走 `dida-cli`
- 这版 skill 不再把其他接入方式作为默认路径

## 与现有 skill 的关系

- 默认自动认证入口就是 `dida-cli`
- 后续任务执行也统一走 `dida-cli`
