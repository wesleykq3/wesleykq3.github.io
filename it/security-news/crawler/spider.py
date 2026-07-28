# -*- coding:utf-8 -*-

import feedparser
import json
import re
from datetime import datetime
import os

# 当前文件路径
CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# security-news目录
BASE_DIR = os.path.dirname(
    CURRENT_DIR
)


# 输出文件
OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "news.json"
)


print("JSON输出位置:")
print(OUTPUT_FILE)

RSS_LIST=[


{
"name":"BleepingComputer",
"url":
"https://www.bleepingcomputer.com/feed/"
},


{
"name":"The Hacker News",
"url":
"https://feeds.feedburner.com/TheHackersNews"
},


{
"name":"CyberSecurityNews",
"url":
"https://cybersecuritynews.com/feed/"
},
{
"name":"krebsonsecurity",
"url":
"https://krebsonsecurity.com/feed/"
},
{
"name":"GBHackers",
"url":
"https://gbhackers.com/feed/"
},
    {
"name":"Phoronix",
"url":
"https://www.phoronix.com/rss.php"
},



]



news=[]



for rss in RSS_LIST:


    print("正在采集:",rss["name"])


    data=feedparser.parse(
        rss["url"]
    )


    for item in data.entries[:10]:


        title=item.title


        summary=""


        if "summary" in item:

            summary=re.sub(
                "<.*?>",
                "",
                item.summary
            )



        if "published" in item:

            date=item.published

        else:

            date=str(
                datetime.now()
            )



        # 提取CVE

        cve=re.findall(

            r"CVE-\d{4}-\d+",

            title

        )



        news.append({


            "title":
            title,


            "date":
            date,


            "url":
            item.link,


            "source":
            rss["name"],


            "summary":
            summary[:200],


            "cve":
            cve


        })




# 按时间排序

news=news[:50]



with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as f:


    json.dump(

        news,

        f,

        ensure_ascii=False,

        indent=4

    )



print(

"新闻更新完成:",

len(news)

)
