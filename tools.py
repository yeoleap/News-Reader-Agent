from crewai.tools import tool
from crewai_tools import SerperDevTool
from playwright.sync_api import sync_playwright
import time
# html 다루고 조작
from bs4 import BeautifulSoup

# TeamBlind 한국 사이트로 검색 제한
search_tool = SerperDevTool(
    search_url="https://google.serper.dev/search",
    n_results=20,
    save_file=False,
    # site: 연산자를 사용하여 특정 사이트로 검색 제한
)

@tool
def scrape_tool(url:str):
    """
    Use this when you need to read the content of a website, in case the website is not available, it returns 'No content'.
    Returns the content of the webpage at the given URL.
    Input should be a string representing the URL.
    for example: "https://www.reuters.com/world/china/cambodia-says-thai-troops-still-occupy-civilian-areas-testing-december-truce-2026-01-14/"
    """

    print(f"Scraping content from URL: {url}")

    try:
        with sync_playwright() as p:
            # 브라우저를 켜고, 페이지로 이동해서, 그 페이지에서 html 추출하고, 정리해야 함 (headers, footers 등 제거)
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--disable-blink-features=AutomationControlled',  # 자동화 탐지 비활성화
                ]
            )

            # User-Agent 및 추가 헤더 설정으로 봇 차단 우회
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080},
                locale='ko-KR',
                timezone_id='Asia/Seoul',
                extra_http_headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Sec-Fetch-User': '?1',
                }
            )
            
            page = context.new_page()
            
            # WebDriver 감지 우회
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """)

            # 타임아웃을 60초로 증가, networkidle 대기로 동적 콘텐츠 로딩 보장
            try:
                page.goto(url, timeout=60000, wait_until="networkidle")
            except:
                # networkidle 실패 시 domcontentloaded로 재시도
                page.goto(url, timeout=60000, wait_until="domcontentloaded")
                time.sleep(3)  # 추가 대기

            # 페이지 스크롤로 lazy-loading 콘텐츠 로드
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)

            html = page.content()

            browser.close()

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
        

        content = soup.get_text(separator=" ", strip=True)
        
        # 공백 정리
        content = " ".join(content.split())

        return content if content != "" else "No content"
        
    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")
        return "No content"