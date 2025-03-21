import json
from typing import Dict, Any, List, Optional
from langchain.tools import BaseTool


class ScriptGenerator(BaseTool):
    """Tool for generating video script concepts based on lead data and video analysis."""

    name: str = "script_generator"
    description: str = """
    Generates video script concepts based on lead data, video analysis, and product requirements.
    Input should be a JSON string containing:
    - lead_data: Lead data with video performance metrics
    - high_performing_videos: List of high-performing videos
    - video_analyses: List of video screenshot analyses
    - product_requirements: Information about the product/campaign
    """
    llm_model: str = "gpt-4o"

    def __init__(self, llm_model: str = "gpt-4o"):
        """Initialize the script generator tool.

        Args:
            llm_model: The LLM model to use for script generation
        """
        super().__init__()
        self.llm_model = llm_model

    def _generate_script_concepts(self,
                                  lead_data: Dict[str, Any],
                                  high_performing_videos: List[Dict[str, Any]],
                                  video_analyses: List[str],
                                  product_requirements: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate script concepts based on input data.

        Args:
            lead_data: Lead data with performance metrics
            high_performing_videos: List of high-performing videos
            video_analyses: List of video screenshot analyses
            product_requirements: Information about the product/campaign

        Returns:
            List of script concepts
        """
        try:
            from openai import OpenAI
            client = OpenAI()

            # Extract relevant information
            creator_name = lead_data.get("nickName", "")

            # Prepare the prompt
            prompt = f"""
            # Video Script Concept Generation
            
            ## Creator Information
            - Creator: {creator_name}
            - Bio: {lead_data.get("bio", "")}
            - Total Followers: {lead_data.get("totalFollowers", "")}
            - Engagement Rate: {lead_data.get("totalEngagementRate", "")}%
            
            ## Performance Metrics
            - Average Views: {lead_data.get("averageViews", 0)}
            - Average Likes: {lead_data.get("averageLikes", 0)}
            - Average Comments: {lead_data.get("averageComments", 0)}
            - Average Shares: {lead_data.get("averageShares", 0)}
            - Tags/Categories: {', '.join(lead_data.get("tags", []))}
            
            ## High-Performing Videos
            {self._format_videos(high_performing_videos)}
            
            ## Video Style Analysis
            {self._format_analyses(video_analyses)}
            
            ## Product/Campaign Information
            - Product Name: {product_requirements.get("product_name", "")}
            - Product Description: {product_requirements.get("product_description", "")}
            - Campaign Goals: {product_requirements.get("campaign_goals", "")}
            - Target Audience: {product_requirements.get("target_audience", "")}
            - Key Messages: {product_requirements.get("key_messages", "")}
            
            ## Your Task
            Based on the creator's high-performing content, visual style analysis, and the product information, generate 3 detailed script concepts for TikTok videos.
            
            For each concept, provide:
            1. A title and format description
            2. A strong hook (first 3 seconds)
            3. A shot-by-shot breakdown with timing
            4. Suggested text overlays and their placement
            5. Music/audio recommendations
            6. A caption strategy with hashtags
            
            Make sure each concept:
            - Matches the creator's authentic style
            - Leverages their high-performing content patterns
            - Naturally integrates the product
            - Has a strong hook and narrative arc
            - Includes specific visual details based on the screenshot analysis
            
            Format each concept as a structured outline with clear sections.
            """

            # Generate script concepts
            response = client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": "You are an expert TikTok content strategist and script developer for influencer marketing campaigns."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )

            # Parse the response
            script_text = response.choices[0].message.content

            # Process the script text into structured concepts
            script_concepts = self._parse_script_concepts(script_text)

            return script_concepts

        except Exception as e:
            print(f"Error generating script concepts: {str(e)}")
            return [{
                "title": "Error generating script concepts",
                "error": str(e)
            }]

    def _format_videos(self, videos: List[Dict[str, Any]]) -> str:
        """Format video information for the prompt.

        Args:
            videos: List of video data dictionaries

        Returns:
            Formatted string with video information
        """
        formatted = ""

        for i, video in enumerate(videos):
            formatted += f"""
            ### Video {i+1}
            - Caption: {video.get("text", "")}
            - Views: {video.get("playCount", 0)}
            - Likes: {video.get("diggCount", 0)}
            - Comments: {video.get("commentCount", 0)}
            - Shares: {video.get("shareCount", 0)}
            - URL: {video.get("webVideoUrl", "")}
            """

        return formatted

    def _format_analyses(self, analyses: List[str]) -> str:
        """Format video analyses for the prompt.

        Args:
            analyses: List of video analysis strings

        Returns:
            Formatted string with analysis information
        """
        formatted = ""

        for i, analysis in enumerate(analyses):
            formatted += f"""
            ### Screenshot Analysis {i+1}
            {analysis}
            
            """

        return formatted

    def _parse_script_concepts(self, script_text: str) -> List[Dict[str, Any]]:
        """Parse script concepts from generated text.

        Args:
            script_text: Generated script text

        Returns:
            List of structured script concepts
        """
        # This is a simple implementation that could be enhanced
        # to better parse structured content from the response
        concepts = []

        # Split by numerical headers (assuming each concept starts with a number)
        parts = script_text.split("# Concept ")

        # Skip the first part if it doesn't contain a concept
        for part in parts[1:] if len(parts) > 1 else parts:
            concept = {
                "title": "",
                "format": "",
                "hook": "",
                "shots": [],
                "text_overlays": [],
                "music": "",
                "caption": ""
            }

            # Extract sections
            lines = part.split("\n")
            current_section = None

            for line in lines:
                line = line.strip()

                if not line:
                    continue

                # Try to identify sections
                if "title" in line.lower() or "format" in line.lower():
                    current_section = "title"
                    concept["title"] = line.split(
                        ":", 1)[1].strip() if ":" in line else line
                elif "hook" in line.lower():
                    current_section = "hook"
                    concept["hook"] = line.split(
                        ":", 1)[1].strip() if ":" in line else ""
                elif "shot" in line.lower() or "breakdown" in line.lower():
                    current_section = "shots"
                elif "text" in line.lower() and "overlay" in line.lower():
                    current_section = "text_overlays"
                elif "music" in line.lower() or "audio" in line.lower():
                    current_section = "music"
                    concept["music"] = line.split(
                        ":", 1)[1].strip() if ":" in line else line
                elif "caption" in line.lower():
                    current_section = "caption"
                    concept["caption"] = line.split(
                        ":", 1)[1].strip() if ":" in line else ""
                elif current_section == "shots" and (":" in line or line.startswith("-")):
                    concept["shots"].append(line.lstrip("- "))
                elif current_section == "text_overlays" and (":" in line or line.startswith("-")):
                    concept["text_overlays"].append(line.lstrip("- "))
                elif current_section == "hook" and not concept["hook"]:
                    concept["hook"] = line
                elif current_section == "caption" and not concept["caption"]:
                    concept["caption"] = line

            concepts.append(concept)

        return concepts

    def _run(self, input_str: str) -> str:
        """Run the script generator tool.

        Args:
            input_str: JSON string containing input data

        Returns:
            JSON string containing generated script concepts
        """
        try:
            # Parse input
            input_json = json.loads(input_str)
            lead_data = input_json.get("lead_data", {})
            high_performing_videos = input_json.get(
                "high_performing_videos", [])
            video_analyses = input_json.get("video_analyses", [])
            product_requirements = input_json.get("product_requirements", {})

            # Generate script concepts
            script_concepts = self._generate_script_concepts(
                lead_data,
                high_performing_videos,
                video_analyses,
                product_requirements
            )

            # Return generated scripts
            return json.dumps({
                "script_concepts": script_concepts
            })

        except Exception as e:
            return json.dumps({"error": str(e)})
