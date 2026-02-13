# News Reader Agent 📰

AI 기반 뉴스 수집 및 분석 에이전트 시스템으로, CrewAI를 활용하여 자동으로 뉴스를 검색하고, 수집하고, 요약하여 큐레이션된 리포트를 생성합니다.

## 🌟 주요 기능

- **자동 뉴스 수집**: Serper API를 통한 Google 검색으로 최신 뉴스 자동 수집
- **지능형 웹 스크래핑**: Playwright 기반의 강력한 웹 스크래핑 (봇 차단 우회 포함)
- **다층 요약**: 헤드라인, 임원 요약, 종합 요약의 3단계 요약 제공
- **큐레이션 리포트**: AI 에이전트가 분석하고 정리한 최종 인사이트 리포트
- **멀티 에이전트 협업**: 전문화된 AI 에이전트들의 협업으로 고품질 결과물 생성

## 🏗️ 시스템 아키텍처

### AI 에이전트

1. **News Hunter Agent** (Senior News Intelligence Specialist)
   - 역할: 최신 뉴스 발견 및 수집
   - 도구: Google Search (Serper), Web Scraper
   - 책임: 신뢰할 수 있는 소스에서 관련성 높은 기사 수집

2. **Summarizer Agent** (Expert News Analyst)
   - 역할: 뉴스 분석 및 요약
   - 도구: Web Scraper
   - 책임: 수집된 기사를 다층 요약으로 변환

3. **Curator Agent** (Strategic Content Curator)
   - 역할: 최종 리포트 큐레이션
   - 책임: 요약된 정보를 종합하여 인사이트 있는 리포트 생성

### 작업 흐름

```
1. Content Harvesting
   └─> Google 검색 → URL 필터링 → 웹 스크래핑 → 품질 검증
   
2. Summarization
   └─> 기사 분석 → 3단계 요약 생성 → 메타데이터 추출
   
3. Final Report Assembly
   └─> 요약 통합 → 인사이트 도출 → 최종 리포트 생성
```

## 📦 설치 방법

### 사전 요구사항

- Python 3.13 이상
- [uv](https://github.com/astral-sh/uv) 패키지 매니저
- Playwright 브라우저 (자동 설치)

### 설치 단계

1. **저장소 클론**
```bash
git clone https://github.com/yeoleap/News-Reader-Agent.git
cd News-Reader-Agent
```

2. **의존성 설치**
```bash
# uv를 사용하여 의존성 설치
uv sync

# Playwright 브라우저 설치
uv run playwright install chromium
```

3. **환경 변수 설정**

`.env` 파일을 생성하고 필요한 API 키를 설정합니다:

```env
# OpenAI API Key (필수)
OPENAI_API_KEY=your_openai_api_key_here

# Serper API Key (Google 검색용, 필수)
SERPER_API_KEY=your_serper_api_key_here

# OpenAI 모델 설정 (선택)
OPENAI_MODEL_NAME=gpt-4o-mini
```

**API 키 발급 방법:**
- OpenAI: https://platform.openai.com/api-keys
- Serper: https://serper.dev/api-key

## 🚀 사용 방법

### 기본 사용

```bash
uv run main.py
```

### 주제 변경

`main.py` 파일에서 `topic`을 원하는 주제로 변경:

```python
result = NewsReaderAgent().crew().kickoff(
    inputs={"topic": "인공지능 최신 뉴스"}  # 여기서 주제 변경
)
```

### 출력 결과

모든 결과는 `output/` 디렉토리에 Markdown 형식으로 저장됩니다:

- `content_harvest.md` - 수집된 뉴스 목록
- `summary.md` - 각 기사의 3단계 요약
- `final_report.md` - 최종 큐레이션 리포트

## 🛠️ 고급 기능

### 웹 스크래핑 기능

`tools.py`의 `scrape_tool`은 다음 기능을 포함합니다:

- ✅ User-Agent 스푸핑
- ✅ WebDriver 감지 우회
- ✅ 동적 콘텐츠 로딩 (networkidle 대기)
- ✅ Lazy-loading 콘텐츠 처리
- ✅ 60초 타임아웃 (긴 로딩 페이지 대응)
- ✅ 자동 에러 핸들링

### 검색 도구 커스터마이징

`tools.py`에서 검색 설정 변경:

```python
search_tool = SerperDevTool(
    n_results=20,      # 검색 결과 개수 (기본: 10)
    save_file=False,   # 검색 결과 파일 저장 여부
)
```

### 에이전트 설정

`config/agents.yaml`에서 각 에이전트의 역할, 목표, 배경 스토리를 커스터마이징할 수 있습니다.

### 작업 흐름 설정

`config/tasks.yaml`에서 각 작업의 설명, 예상 출력, 필터링 기준 등을 수정할 수 있습니다.

## 📊 프로젝트 구조

```
news-reader-agent/
├── config/
│   ├── agents.yaml          # AI 에이전트 설정
│   └── tasks.yaml           # 작업 흐름 정의
├── output/                  # 생성된 리포트 저장 위치
│   ├── content_harvest.md
│   ├── summary.md
│   └── final_report.md
├── main.py                  # 메인 실행 파일
├── tools.py                 # 검색 및 스크래핑 도구
├── pyproject.toml          # 프로젝트 의존성
├── .env                     # 환경 변수 (생성 필요)
└── README.md               # 이 파일
```

## 🔧 기술 스택

- **AI Framework**: [CrewAI](https://github.com/joaomdmoura/crewAI) - 멀티 에이전트 오케스트레이션
- **LLM**: OpenAI GPT-4 / GPT-4o-mini
- **검색**: Serper API (Google Search)
- **웹 스크래핑**: Playwright
- **HTML 파싱**: BeautifulSoup4
- **패키지 관리**: uv

## 📝 사용 예시

### 예시 1: 기술 뉴스 수집

```python
result = NewsReaderAgent().crew().kickoff(
    inputs={"topic": "AI and Machine Learning"}
)
```

### 예시 2: 특정 이벤트 분석

```python
result = NewsReaderAgent().crew().kickoff(
    inputs={"topic": "CES 2026"}
)
```

## 🤝 기여하기

기여는 언제나 환영합니다! 다음 절차를 따라주세요:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ 주의사항

- API 사용량에 따라 비용이 발생할 수 있습니다 (OpenAI, Serper)
- 웹 스크래핑 시 대상 사이트의 robots.txt와 이용 약관을 준수하세요
- 과도한 요청으로 IP가 차단될 수 있으니 적절한 간격을 두고 사용하세요

## 📄 라이선스

This project is licensed under the MIT License.

## 👤 작성자

**yeoleap**

- GitHub: [@yeoleap](https://github.com/yeoleap)
- Repository: [News-Reader-Agent](https://github.com/yeoleap/News-Reader-Agent)

## 🙏 감사의 말

- [CrewAI](https://github.com/joaomdmoura/crewAI) - 멋진 멀티 에이전트 프레임워크
- [Playwright](https://playwright.dev/) - 강력한 브라우저 자동화 도구
- [Serper](https://serper.dev/) - Google 검색 API

---

**⭐ 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**
