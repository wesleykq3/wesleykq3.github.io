# -*- coding: utf-8 -*-

"""
Security News RSS Collector

功能:
1. 获取安全新闻RSS
2. 提取标题
3. 提取发布日期
4. 提取文章链接
5. 生成 news.json

适用于:
GitHub Actions + GitHub Pages
"""


import os
import json
import feedparser
from datetime import datetime



# ==================================================
# 路径配置
# ==================================================

# 当前文件:
# it/security-news/crawler/spider.py

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# security-news目录

BASE_DIR = os.path.dirname(
    CURRENT_DIR
)


# 输出:

# it/security-news/news.json

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "news.json"
)



print("当前脚本目录:")
print(CURRENT_DIR)

print("JSON输出:")
print(OUTPUT_FILE)



# ==================================================
# RSS源配置
# ==================================================

RSS_LIST = [

    {
        "name": "The Hacker News",
        "url":
        "https://feeds.feedburner.com/TheHackersNews"
    },


    {
        "name": "BleepingComputer",
        "url":
        "https://www.bleepingcomputer.com/feed/"
    },


    {
        "name": "Cybersecurity News",
        "url":
        "https://cybersecuritynews.com/feed/"
    },


    {
        "name": "SecurityWeek",
        "url":
        "https://www.securityweek.com/feed/"
    }

]



# ==================================================
# 日期处理
# ==================================================

def format_date(entry):

    """
    统一日期格式
    """

    try:

        if hasattr(entry, "published_parsed"):

            dt = datetime(
                *entry.published_parsed[:6]
            )

            return dt.strftime(
                "%Y-%m-%d"
            )


    except Exception:

        pass


    return datetime.now().strftime(
        "%Y-%m-%d"
    )



# ==================================================
# 获取新闻
# ==================================================

def fetch_news():

    news_list = []


    for rss in RSS_LIST:


        print(
            "正在获取:",
            rss["name"]
        )


        try:


            feed = feedparser.parse(
                rss["url"]
            )


            count = 0


            for item in feed.entries:


                if count >= 10:

                    break



                news = {


                    "source":
                    rss["name"],



                    "title":
                    item.get(
                        "title",
                        ""
                    ),



                    "date":
                    format_date(
                        item
                    ),



                    "url":
                    item.get(
                        "link",
                        ""
                    )

                }


                news_list.append(
                    news
                )


                count += 1



        except Exception as e:


            print(
                rss["name"],
                "错误:",
                e
            )



    return news_list



# ==================================================
# 保存JSON
# ==================================================

def save_json(data):


    os.makedirs(
        BASE_DIR,
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=4

        )



    print(
        "生成完成:",
        OUTPUT_FILE
    )



# ==================================================
# 主程序
# ==================================================

if __name__ == "__main__":


    news = fetch_news()


    print(
        "新闻数量:",
        len(news)
    )


    save_json(
        news
    )
