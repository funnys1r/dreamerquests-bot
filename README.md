在此注册：https://dreamerquests.partofdream.io/login?referralCodeForPOD=6aa5decd（使用 Twitter 登录）
不要忘记连接社交并完成任务！
账户用户ID和Cookies
Python3 最新版

# DreamerQuest 自动签到工具

这是一个用于 [Part of Dream](https://dreamerquests.partofdream.io/) 的自动签到和抽奖工具。

## 功能特点

- ✨ 支持多账号管理
- 🔄 支持多代理自动切换
- 🎲 随机延迟执行（避免固定时间）
- 📝 简单的配置文件格式
- 🔒 安全的 Cookie 管理
- 🌈 彩色日志输出

## 使用前准备

1. 安装 Python 3.x
2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 配置说明

### 1. 账号配置 (config.txt)

每行一个账号，格式为：
```
账号备注:用户ID:connect.sid
```

例如：
```
账号1:_ID:s%3Axxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
账号2:_ID:s%3Ayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
```

### 2. 代理配置 (proxies.txt)

每行一个代理地址，支持以下格式：
```
http://127.0.0.1:7890
http://用户名:密码@127.0.0.1:7890
```

如果不需要使用代理，可以清空文件内容或者在每行前面加 # 注释。

## 获取账号信息

1. 登录 [DreamerQuest](https://dreamerquests.partofdream.io/)
2. 按 F12 打开开发者工具
3. 切换到 Network（网络）标签
4. 刷新页面
5. 找到 session 请求
6. 从 Response 中复制 userId
7. 从 Request Headers 的 Cookie 中复制 connect.sid 的值

## 运行方法

```bash
python main.py
```

程序会：
1. 首次运行时立即执行所有账号的签到和抽奖
2. 之后每24小时 + 随机1-60分钟执行一次
3. 每个账号的执行时间都会有随机延迟，避免同时请求

## 注意事项

1. 确保 config.txt 中的账号信息正确
2. 如果使用代理，确保代理地址可用
3. 程序会自动处理"今日已完成"的情况
4. 使用 Ctrl+C 可以安全退出程序

## 日志说明

程序运行时会显示彩色日志，包含：
- 账号加载信息
- 签到/抽奖状态
- 代理使用情况
- 下次执行时间

## 许可证

MIT License

## 免责声明

本工具仅供学习和研究使用，使用本工具所造成的任何后果由使用者自行承担。 