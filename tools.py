from crewai.tools import tool
from crewai_tools import SerperDevTool
from playwright.sync_api import sync_playwright
import time
# html 다루고 조작
from bs4 import BeautifulSoup

search_tool = SerperDevTool()

print(search_tool.run(search_query="Cambodia thai war"))    

@tool
def scrape_tool(url:str):
    """
    Use this when you need to read the content of a website, in case the website is not available, it returns 'No content'.
    Returns the content of the webpage at the given URL.
    Input should be a string representing the URL.
    for example: "https://www.reuters.com/world/china/cambodia-says-thai-troops-still-occupy-civilian-areas-testing-december-truce-2026-01-14/"
    """

    print(f"Scraping content from URL: {url}")

    with sync_playwright() as p:
        # 브라우저를 켜고, 페이지로 이동해서, 그 페이지에서 html 추출하고, 정리해야 함 (headers, footers 등 제거)
        browswer = p.chromium.launch(headless=True)

        page = browswer.new_page()

        page.goto(url)

        time.sleep(5)  # 페이지가 로드될 시간을 줌

        html = page.content()

        browswer.close()

        soup = BeautifulSoup(html, 'html.parser')

        unwanted_tags = [
            "header",
            "footer",
            "nav",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "select",
            "textarea",
            "img",
            "svg",
            "canvas",
            "audio",
            "video",
            "embed",
            "object",
        ]

        for tag in soup.find_all(unwanted_tags):
            # 페이지 element 와 children 를 제거
            tag.decompose()
        

        content = soup.get_text(separator=" ")

        return content if content != "" else "No content"