# -*- coding:utf-8 -*-

import feedparser
import json
import re
from datetime import datetime



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
}



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

"news.json",

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
