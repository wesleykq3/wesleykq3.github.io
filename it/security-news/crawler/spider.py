# -*- coding: utf-8 -*-

"""
Security News RSS Collector

运行环境:
GitHub Actions

功能:
1. RSS新闻采集
2. 提取标题
3. 提取日期
4. 提取URL
5. 生成news.json

输出:
it/security-news/news.json
"""


import os
import json
import feedparser

from datetime import datetime



# ==================================================
# 路径配置
# ==================================================

# 当前:
# it/security-news/crawler/spider.py

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# 当前:
# it/security-news/crawler

# 上一级:
# it/security-news

BASE_DIR = os.path.dirname(
    CURRENT_DIR
)



OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "news.json"
)



print("==============================")
print("Python运行目录:")
print(os.getcwd())


print("脚本目录:")
print(CURRENT_DIR)


print("JSON输出路径:")
print(OUTPUT_FILE)

print("==============================")



# ==================================================
# RSS配置
# ==================================================

RSS_SOURCES = [

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
        "name": "Cyber Security News",
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
# 日期格式化
# ==================================================

def get_date(entry):


    try:

        if hasattr(
            entry,
            "published_parsed"
        ):


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
# RSS采集
# ==================================================

def fetch_news():


    news_list = []


    for source in RSS_SOURCES:


        print(
            "\n正在获取:",
            source["name"]
        )


        try:


            feed = feedparser.parse(
                source["url"]
            )



            if not feed.entries:


                print(
                    "没有获取到新闻"
                )

                continue



            count = 0



            for item in feed.entries:



                if count >= 10:

                    break



                news = {


                    "source":
                    source["name"],



                    "title":
                    item.get(
                        "title",
                        ""
                    ),



                    "date":
                    get_date(
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
                "RSS错误:",
                source["name"],
                e
            )



    return news_list



# ==================================================
# 保存JSON
# ==================================================

def save_json(news):


    # 确保目录存在

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

            news,

            f,

            ensure_ascii=False,

            indent=4

        )



    print(
        "\nJSON生成成功:"
    )

    print(
        OUTPUT_FILE
    )



# ==================================================
# 主程序
# ==================================================

if __name__ == "__main__":



    print(
        "\n开始采集安全新闻..."
    )



    news = fetch_news()



    print(
        "\n新闻数量:",
        len(news)
    )



    save_json(
        news
    )



    print(
        "\n任务完成"
    )
