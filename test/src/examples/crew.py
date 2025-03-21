from tools.script_generator import ScriptGenerator
from tools.mongodb_client import MongoDBClient
from tools.tiktok_analyzer import TikTokVideoAnalyzer
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import agentstack
import sys
import os

# Add parent directory to path to import tools
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@CrewBase
class TestCrew():
    """test crew"""

    @task
    def identify_plan_of_action(self) -> Task:
        return Task(
            config=self.tasks_config['identify_plan_of_action'],
        )

    @task
    def find_solution(self) -> Task:
        return Task(
            config=self.tasks_config['find_solution'],
        )

    @task
    def check_solution(self) -> Task:
        return Task(
            config=self.tasks_config['check_solution'],
        )

    @task
    def generate_script_concepts(self) -> Task:
        return Task(
            config=self.tasks_config['generate_script_concepts'],
        )

    @agent
    def manager(self) -> Agent:
        return Agent(
            config=self.agents_config['manager'],
            tools=[],  # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @agent
    def triage(self) -> Agent:
        return Agent(
            config=self.agents_config['triage'],
            tools=[],  # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @agent
    def worker(self) -> Agent:
        return Agent(
            config=self.agents_config['worker'],
            tools=[],  # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @agent
    def fact_checker(self) -> Agent:
        return Agent(
            config=self.agents_config['fact_checker'],
            tools=[],  # add tools here or use `agentstack tools add <tool_name>
            verbose=True,
        )

    @agent
    def script_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['script_generator'],
            tools=[
                TikTokVideoAnalyzer(),
                MongoDBClient(),
                ScriptGenerator()
            ],
            verbose=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Test crew"""
        # Filter out the manager from the agents list
        agents_without_manager = [
            a for a in self.agents if a.role != self.manager().role]
        return Crew(
            agents=agents_without_manager,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.manager(),
            verbose=True,
        )
