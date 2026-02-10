import dotenv

dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, agent, task, crew

@CrewBase
class TranslatorCrew:
    
    # agent 를 만드려면 함수에 agent decorator 를 붙여야 한다.
    @agent
    def translator_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["translator_agent"]
        )

    @task
    def translate_task(self):
        return Task(
            config=self.tasks_config["translate_task"]
        )
    @task
    def retranslate_task(self):
        return Task(
            config=self.tasks_config["retranslate_task"]
        )   
    @crew
    def assemble_crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            # Enable verbose mode for detailed logging
            verbose=True
        )
    
TranslatorCrew().assemble_crew().kickoff(inputs={"sentence": "I'm daeyeol and I like to ride my bicicle in napoli"})