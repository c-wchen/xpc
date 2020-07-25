## 新片场爬虫
> 爬取范围, 评论和主页信息（覆盖video图片和video链接）

```bash
│  README.md
│  requirements.txt   需要安装包资源
│  scrapy.cfg
│  xpc.sql            新片场数据库设计
└─xpc
    │  items.py      
    │  middlewares.py  
    │  pipelines.py   item管道
    │  run.py
    │  settings.py  
    │  __init__.py
    │
    ├─spiders
       │  discovery.py
       │  __init__.py
       │
       └─__pycache__
               discovery.cpython-37.pyc
               __init__.cpython-37.pyc
```

## 相关难点解决
1. 429 too many requests
```python
# 在setting中添加请求频率
DOWNLOAD_DELAY = 1
# 单个IP的最大请求值
CONCURRENT_REQUESTS_PER_IP = 16
```
2. 通过debug调试报错
```python
# run.py 使用run.py代替运行脚本
from scrapy import cmdline
cmdline.execute('scrapy crawl discovery'.split(' '))
```

## 可以修改配置
1. 数据库配置
* 创建数据库 xpc 
* pipelines.py配置数据库host、user、password
* 开启MySQLPipeline

2. scrapy-redis配置

```python
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
REDIS_URL = 'redis://:password@106.14.136.195:6379'
SCHEDULER_PERSIST = True
```