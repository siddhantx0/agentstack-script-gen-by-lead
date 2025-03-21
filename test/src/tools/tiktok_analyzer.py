import os
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import base64
import requests
from langchain.tools import BaseTool


class TikTokVideoAnalyzer(BaseTool):
    """Tool for analyzing TikTok videos and capturing screenshots."""

    name: str = "tiktok_video_analyzer"
    description: str = """
    Analyzes TikTok videos by capturing screenshots and extracting visual information.
    Input should be a JSON string containing:
    - video_url: The URL of the TikTok video to analyze
    - num_screenshots: Number of screenshots to capture (default: 5)
    """
    vision_model: str = "gpt-4o"
    screenshot_dir: Path = None

    def __init__(self, vision_model: str = "gpt-4o"):
        """Initialize the TikTok video analyzer tool.

        Args:
            vision_model: The vision model to use for analyzing screenshots
        """
        super().__init__()
        self.vision_model = vision_model
        self.screenshot_dir = Path("data/screenshots")
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

    def _setup_driver(self) -> webdriver.Chrome:
        """Set up and return a Chrome webdriver with appropriate options."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument(
            "--window-size=393,852")  # Mobile size for TikTok
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")

        return webdriver.Chrome(options=chrome_options)

    def _capture_screenshots(self, driver: webdriver.Chrome, video_url: str, num_screenshots: int = 5) -> List[str]:
        """Capture screenshots of a TikTok video at different timestamps.

        Args:
            driver: The Chrome webdriver
            video_url: The URL of the TikTok video
            num_screenshots: Number of screenshots to capture

        Returns:
            List of screenshot file paths
        """
        try:
            driver.get(video_url)

            # Wait for video to load
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )

            # Get video element and video duration
            video = driver.find_element(By.TAG_NAME, "video")

            # Click to start playing
            video.click()
            time.sleep(2)  # Wait for video to start

            # Get video duration using JavaScript
            video_duration = driver.execute_script(
                "return arguments[0].duration", video)
            if not video_duration or video_duration <= 0:
                video_duration = 15  # Default to 15 seconds if can't determine

            # Calculate screenshot timestamps
            timestamps = [i * video_duration /
                          (num_screenshots + 1) for i in range(1, num_screenshots + 1)]

            screenshot_paths = []
            for i, timestamp in enumerate(timestamps):
                # Set video time to timestamp
                driver.execute_script(
                    f"arguments[0].currentTime = {timestamp}", video)
                time.sleep(0.5)  # Wait for frame to render

                # Take screenshot
                screenshot = driver.get_screenshot_as_png()
                screenshot_path = self.screenshot_dir / \
                    f"{Path(video_url).name.split('?')[0]}_{i}.png"

                # Save screenshot
                with open(screenshot_path, "wb") as f:
                    f.write(screenshot)

                screenshot_paths.append(str(screenshot_path))

            return screenshot_paths

        except Exception as e:
            print(f"Error capturing screenshots: {str(e)}")
            return []

    def _analyze_screenshots(self, screenshot_paths: List[str]) -> Dict[str, Any]:
        """Analyze screenshots using a vision model to extract visual information.

        Args:
            screenshot_paths: List of screenshot file paths

        Returns:
            Dictionary containing analysis results
        """
        # This would normally use the OpenAI API to analyze the images
        # For now, returning a placeholder implementation

        try:
            from openai import OpenAI
            client = OpenAI()

            # Convert images to base64
            image_contents = []
            for path in screenshot_paths:
                with open(path, "rb") as image_file:
                    encoded_image = base64.b64encode(
                        image_file.read()).decode('utf-8')
                    image_contents.append(encoded_image)

            # Prepare the prompt for visual analysis
            prompt = """
            Analyze this TikTok video screenshot and describe:
            1. What's happening in the video
            2. Visual style elements (colors, lighting, composition)
            3. Text overlays and their positioning
            4. Subject's positioning and body language
            5. Any props or focal objects visible
            Provide specific details that would be helpful for recreating a similar visual style.
            """

            # Analyze each screenshot
            analyses = []
            for encoded_image in image_contents:
                response = client.chat.completions.create(
                    model=self.vision_model,
                    messages=[
                        {"role": "system", "content": "You are an expert video content analyst specializing in TikTok creator content."},
                        {"role": "user", "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {
                                "url": f"data:image/png;base64,{encoded_image}"}}
                        ]}
                    ],
                    max_tokens=500
                )
                analyses.append(response.choices[0].message.content)

            return {
                "screenshot_analyses": analyses,
                "screenshots": screenshot_paths
            }

        except Exception as e:
            print(f"Error analyzing screenshots with vision model: {str(e)}")
            return {
                "screenshot_analyses": ["Error analyzing screenshots"],
                "screenshots": screenshot_paths
            }

    def _run(self, input_str: str) -> str:
        """Run the TikTok video analyzer tool.

        Args:
            input_str: JSON string containing video_url and optionally num_screenshots

        Returns:
            JSON string containing analysis results
        """
        try:
            # Parse input
            input_json = json.loads(input_str)
            video_url = input_json.get("video_url")
            num_screenshots = input_json.get("num_screenshots", 5)

            if not video_url:
                return json.dumps({"error": "Video URL is required"})

            # Set up webdriver
            driver = self._setup_driver()

            try:
                # Capture screenshots
                screenshot_paths = self._capture_screenshots(
                    driver, video_url, num_screenshots)

                if not screenshot_paths:
                    return json.dumps({"error": "Failed to capture screenshots"})

                # Analyze screenshots
                analysis_results = self._analyze_screenshots(screenshot_paths)

                return json.dumps(analysis_results)

            finally:
                # Clean up
                driver.quit()

        except Exception as e:
            return json.dumps({"error": str(e)})
