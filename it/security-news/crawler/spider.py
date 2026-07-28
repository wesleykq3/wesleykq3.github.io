import os
import json


# 当前文件目录
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


print("JSON输出路径:", OUTPUT_FILE)


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
