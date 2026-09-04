# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os


# =========================
# 当前文件所在目录
# 例如：
# security-news/crawler/
# =========================

CURRENT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# =========================
# security-news 根目录
# =========================

BASE_DIR = os.path.dirname(
    CURRENT_DIR
)


# =========================
# JSON 输出文件
#
# 最终路径：
# security-news/ai_status.json
# =========================

OUTPUT_FILE = os.path.join(
    BASE_DIR,
    "ai_status.json"
)


print("AI Status JSON输出位置:")
print(OUTPUT_FILE)


# =========================
# 配置
# =========================

TIMEOUT = 10


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/130.0.0.0 "
        "Safari/537.36"
    )
}


# =========================
# 通用 Statuspage JSON
# =========================

def get_statuspage_json(
    name,
    url
):

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        status = data.get(
            "status",
            {}
        )

        return {

            "service": name,

            "status": status.get(
                "indicator",
                "unknown"
            ),

            "description": status.get(
                "description",
                "Unknown"
            ),

            "url": url

        }

    except Exception as e:

        return {

            "service": name,

            "status": "unknown",

            "description": str(e),

            "url": url

        }


# =========================
# OpenAI
# =========================

def check_openai():

    url = "https://status.openai.com/"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            " ",
            strip=True
        )

        text = text.lower()

        if (
            "fully operational" in text
            or "all systems operational" in text
        ):

            status = "operational"

        elif (
            "experiencing issues" in text
            or "degraded performance" in text
        ):

            status = "degraded"

        elif (
            "major outage" in text
            or "outage" in text
        ):

            status = "outage"

        else:

            status = "unknown"


        return {

            "service": "OpenAI",

            "status": status,

            "description": "OpenAI Status Page",

            "url": url

        }


    except Exception as e:

        return {

            "service": "OpenAI",

            "status": "unknown",

            "description": str(e),

            "url": url

        }


# =========================
# Claude
# =========================

def check_claude():

    return get_statuspage_json(

        "Claude",

        "https://status.claude.com/api/v2/status.json"

    )


# =========================
# Claude Components
# =========================

def check_claude_components():

    url = (
        "https://status.claude.com/"
        "api/v2/components.json"
    )


    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        components = []


        for item in data.get(
            "components",
            []
        ):

            components.append({

                "name": item.get(
                    "name"
                ),

                "status": item.get(
                    "status"
                )

            })


        return components


    except Exception as e:

        print(
            "Claude Components 获取失败:",
            str(e)
        )

        return []


# =========================
# Gemini
# =========================
def check_gemini():
    url = "https://aistudio.google.com/status"

    try:
        response = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=(10, 30)
        )

        response.raise_for_status()

        text = response.text.lower()

        # 根据官方状态页面内容进行简单判断
        if "resolved" in text and "issue has been resolved" in text:
            status = "operational"
            description = "Google AI Studio / Gemini API 当前没有正在处理的故障"

        elif "investigating" in text:
            status = "degraded"
            description = "Google AI Studio / Gemini API 正在调查问题"

        elif "identified" in text:
            status = "degraded"
            description = "Google AI Studio / Gemini API 已确认存在问题"

        elif "monitoring" in text:
            status = "degraded"
            description = "Google AI Studio / Gemini API 正在监控问题恢复情况"

        else:
            status = "operational"
            description = "Google AI Studio Status 页面可正常访问"

        return {
            "service": "Gemini / Google AI Studio",
            "status": status,
            "description": description,
            "url": url,
            "http_status": response.status_code
        }

    except requests.exceptions.Timeout:
        return {
            "service": "Gemini / Google AI Studio",
            "status": "unknown",
            "description": "访问 Google AI Studio Status 页面超时",
            "url": url
        }

    except Exception as e:
        return {
            "service": "Gemini / Google AI Studio",
            "status": "unknown",
            "description": str(e),
            "url": url
        }
# =========================
# Grok / xAI
# =========================

def check_grok():

    url = "https://status.x.ai/"


    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        text = response.text.lower()


        if (
            "no incidents declared" in text
            or "fully operational" in text
            or "all systems operational" in text
        ):

            status = "operational"


        elif (
            "major outage" in text
            or "outage" in text
        ):

            status = "outage"


        elif (
            "degraded performance" in text
            or "degraded" in text
            or "disruption" in text
        ):

            status = "degraded"


        elif "maintenance" in text:

            status = "maintenance"


        else:

            status = "unknown"


        return {

            "service": "Grok / xAI",

            "status": status,

            "description": "xAI Status Page",

            "url": url

        }


    except Exception as e:

        return {

            "service": "Grok / xAI",

            "status": "unknown",

            "description": str(e),

            "url": url

        }


# =========================
# 打印状态
# =========================

def print_status(
    result
):

    print("=" * 60)

    print(
        f"Service     : "
        f"{result['service']}"
    )

    print(
        f"Status      : "
        f"{result['status']}"
    )

    print(
        f"Description : "
        f"{result['description']}"
    )

    print(
        f"URL         : "
        f"{result['url']}"
    )


# =========================
# 主程序
# =========================

def main():

    print()

    print("=" * 60)

    print(
        "AI 服务状态监控"
    )

    print(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    print("=" * 60)


    # =====================
    # 保存所有服务状态
    # =====================

    results = []


    print(
        "\n正在检查 OpenAI..."
    )

    results.append(
        check_openai()
    )


    print(
        "正在检查 Claude..."
    )

    results.append(
        check_claude()
    )


    print(
        "正在检查 Gemini..."
    )

    results.append(
        check_gemini()
    )


    print(
        "正在检查 Grok / xAI..."
    )

    results.append(
        check_grok()
    )


    # =====================
    # 打印结果
    # =====================

    print()

    for result in results:

        print_status(
            result
        )


    # =====================
    # Claude Components
    # =====================

    print("=" * 60)

    print(
        "\n正在获取 Claude Components..."
    )


    components = (
        check_claude_components()
    )


    for item in components:

        print(

            f"{item['name']}: "

            f"{item['status']}"

        )


    # =====================
    # JSON 数据
    # =====================

    output = {

        "timestamp":
        datetime.now().isoformat(),

        "services":
        results,

        "claude_components":
        components

    }


    # =====================
    # 保存 JSON
    # =====================

    try:

        with open(
            OUTPUT_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                output,

                f,

                ensure_ascii=False,

                indent=4

            )


        print()

        print("=" * 60)

        print(
            "AI 服务状态已保存"
        )

        print(
            OUTPUT_FILE
        )

        print("=" * 60)


    except Exception as e:

        print(
            "保存 JSON 失败:"
        )

        print(
            str(e)
        )


# =========================
# 程序入口
# =========================

if __name__ == "__main__":

    main()
