from crewai import Agent, Crew, Process, Task, tools
from crewai.project import CrewBase, agent, crew, task
import agentstack
import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


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
        """Create an agent specialized in generating creative scripts for TikTok videos."""
        # Create custom tools using crewai's tool function
        @tools.tool
        def tiktok_video_analyzer(video_url: str, num_screenshots: int = 5) -> str:
            """
            Analyzes TikTok videos by capturing screenshots and extracting visual information.

            Args:
                video_url: The URL of the TikTok video to analyze
                num_screenshots: Number of screenshots to capture (default: 5)

            Returns:
                JSON string containing analysis results
            """
            # Mock implementation for now
            return json.dumps({
                "screenshot_analyses": [
                    "The video shows a creator demonstrating a product with bright lighting and colorful background.",
                    "Close-up shot of product with on-screen text describing features."
                ],
                "screenshots": ["path/to/screenshot1.png", "path/to/screenshot2.png"]
            })

        @tools.tool
        def mongodb_client(lead_id: str, collection: str = "leads") -> str:
            """
            Fetches and processes lead data from MongoDB.

            Args:
                lead_id: The MongoDB ObjectId of the lead to fetch
                collection: The MongoDB collection to query (default: 'leads')

            Returns:
                JSON string containing lead data and analytics
            """
            # Mock implementation using environment variables
            mongodb_uri = os.environ.get("MONGODB_URI", "")
            if not mongodb_uri:
                return json.dumps({"error": "MongoDB connection string is required"})

            # Return mock data for now
            return json.dumps({
                "lead_data": {
                    "id": lead_id,
                    "nickName": "CreativeTikToker",
                    "bio": "Creating awesome content daily!",
                    "totalFollowers": 50000
                },
                "high_performing_videos": [
                    {"text": "My best outfit of the day!",
                        "playCount": 100000, "diggCount": 20000}
                ],
                "performance_metrics": {
                    "avg_views": 75000,
                    "avg_likes": 15000
                }
            })

        @tools.tool
        def script_generator(lead_data: dict, high_performing_videos: list, video_analyses: list, product_requirements: dict) -> str:
            """
            Generates video script concepts based on lead data, video analysis, and product requirements.

            Args:
                lead_data: Lead data with video performance metrics
                high_performing_videos: List of high-performing videos
                video_analyses: List of video screenshot analyses
                product_requirements: Information about the product/campaign

            Returns:
                JSON string containing generated script concepts
            """
            # Mock implementation for script generation
            return json.dumps({
                "script_concepts": [
                    {
                        "title": "Day-to-Night Transformation with StyleBoost",
                        "format": "Before/After Transformation",
                        "hook": "Ever feel stuck with the same outfit all day? Watch this!",
                        "shots": [
                            "0:00-0:03: Creator looking frustrated at outfit in mirror",
                            "0:04-0:08: Creator shows StyleBoost accessories",
                            "0:09-0:15: Quick transformation with accessories"
                        ],
                        "text_overlays": [
                            "POV: When you have meetings AND dinner plans",
                            "StyleBoost - One outfit, endless possibilities"
                        ],
                        "music": "Upbeat transformation music",
                        "caption": "One outfit, endless possibilities with @StyleBoost! #fashionhack #styletips"
                    }
                ]
            })

        return Agent(
            config=self.agents_config['script_generator'],
            tools=[
                tiktok_video_analyzer,
                mongodb_client,
                script_generator
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
