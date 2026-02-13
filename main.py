import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew
from tools import search_tool, scrape_tool

@CrewBase
class NewsReaderAgent:
    
    # agent 를 만드려면 함수에 agent decorator 를 붙여야 한다.
    @agent
    def news_hunter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["news_hunter_agent"],
            tools=[search_tool, scrape_tool]
        )
    
    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["summarizer_agent"],
            tools=[scrape_tool]
        )

    @agent
    def curator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["curator_agent"]
        )

    @task
    def content_harvesting_task(self):
        return Task(
            config=self.tasks_config["content_harvesting_task"]
        )  
    # 위 task 의 output이 아래 task 의 input 으로 들어감
    @task
    def summarization_task(self):
        return Task(
            config=self.tasks_config["summarization_task"]
        )    
    
    @task
    def final_report_assembly_task(self):
        return Task(
            config=self.tasks_config["final_report_assembly_task"]
        ) 
    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            # Enable verbose mode for detailed logging
            verbose=True
        )

# NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thai War"})

## 각 개별 작업의 출력에 접근하는 방법
result = NewsReaderAgent().crew().kickoff(inputs={"topic": "Cambodia Thai War"})

for task_output in result.tasks_output:
    print(task_output)