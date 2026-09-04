import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json


TIMEOUT = 10

HEADERS = {
    "User-Agent": "Mozilla/5.0 AI-Service-Monitor/1.0"
}


def get_statuspage_json(name, url):
    """
    通用 Atlassian Statuspage JSON API
    适用于 Claude 等服务
    """

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        status = data.get("status", {})

        return {
            "service": name,
            "status": status.get("indicator", "unknown"),
            "description": status.get("description", "Unknown"),
            "url": url
        }

    except Exception as e:

        return {
            "service": name,
            "status": "unknown",
            "description": str(e),
            "url": url
        }


def check_openai():
    """
    检查 OpenAI Status
    """

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

        if "fully operational" in text.lower():

            status = "operational"

        elif "experiencing issues" in text.lower():

            status = "degraded"

        elif "outage" in text.lower():

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


def check_claude():

    return get_statuspage_json(
        "Claude",
        "https://status.claude.com/api/v2/status.json"
    )


def check_claude_components():

    url = "https://status.claude.com/api/v2/components.json"

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

        components = []

        for item in data.get("components", []):

            components.append({
                "name": item.get("name"),
                "status": item.get("status")
            })

        return components

    except Exception as e:

        return []


def check_gemini():

    url = "https://www.google.com/appsstatus/dashboard/"

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

        # Google 状态页面结构可能变化
        # 这里只检查 Gemini 是否存在
        if "Gemini" in text:

            status = "check_dashboard"

            description = (
                "Gemini found in Google Workspace "
                "Status Dashboard"
            )

        else:

            status = "unknown"

            description = (
                "Gemini status not detected"
            )

        return {
            "service": "Gemini",
            "status": status,
            "description": description,
            "url": url
        }

    except Exception as e:

        return {
            "service": "Gemini",
            "status": "unknown",
            "description": str(e),
            "url": url
        }


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

        if "no incidents declared" in text:

            status = "operational"

        elif "fully operational" in text:

            status = "operational"

        elif "outage" in text:

            status = "outage"

        elif "disruption" in text:

            status = "degraded"

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


def print_status(result):

    print("=" * 60)

    print(
        f"Service     : {result['service']}"
    )

    print(
        f"Status      : {result['status']}"
    )

    print(
        f"Description : {result['description']}"
    )

    print(
        f"URL         : {result['url']}"
    )


def main():

    print("\nAI 服务状态监控")

    print(
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    results = []

    results.append(
        check_openai()
    )

    results.append(
        check_claude()
    )

    results.append(
        check_gemini()
    )

    results.append(
        check_grok()
    )

    for result in results:

        print_status(result)

    print("=" * 60)

    print("\nClaude Components:")

    components = check_claude_components()

    for item in components:

        print(
            f"{item['name']}: "
            f"{item['status']}"
        )

    # 保存 JSON

    output = {
        "timestamp": datetime.now().isoformat(),
        "services": results,
        "claude_components": components
    }

    with open(
        "ai_status.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(
        "\n结果已保存到 ai_status.json"
    )


if __name__ == "__main__":

    main()