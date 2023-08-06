# StarBot

一款极速，多功能的哔哩哔哩推送机器人。

## 特性

* 极速的直播推送，通过连接直播间实现
* 接近于手机端效果的绘图式动态推送
* 详细的直播数据统计
* 群内数据查询、榜单查询

## 快速开始

项目依赖于 Redis 数据库进行持久化的数据存储，依赖于 Mirai 和 mirai-http 进行消息推送

### 安装

```shell
pip install starbot-bilibili
```

### 启动

推送配置的 JSON 文件可使用 [官网](https://bot.starlwr.com/depoly/json) 的在线制作工具生成

```python
from starbot.core.bot import StarBot
from starbot.core.datasource import JsonDataSource
from starbot.utils import config

config.set_credential(sessdata="B站账号的sessdata", bili_jct="B站账号的bili_jct", buvid3="B站账号的buvid3")

datasource = JsonDataSource("推送配置.json")
bot = StarBot(datasource)
bot.run()
```

详细文档请参见 [部署文档](https://bot.starlwr.com/depoly/document)
