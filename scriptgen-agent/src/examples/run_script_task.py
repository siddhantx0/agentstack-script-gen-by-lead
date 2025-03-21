#!/usr/bin/env python
from crew import TestCrew
import os
import sys
import json
from dotenv import load_dotenv

# Add the current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from the local crew.py

# Load environment variables
load_dotenv()


def main():
    """
    Run only the script generation task directly.

    This is useful for testing the script generator functionality
    without running the full crew pipeline.
    """
    # Create the crew instance
    crew_instance = TestCrew().crew()

    # Set up input data
    lead_id = sys.argv[1] if len(sys.argv) > 1 else "67d109795a08effb5160dcf0"
    product_name = sys.argv[2] if len(
        sys.argv) > 2 else "StyleBoost Accessory Set"

    # Create inputs with the provided lead ID and product info
    inputs = {
        "query": f"Generate video script concepts for creator with lead ID {lead_id} and product '{product_name}'",
        "lead_data": {
            "id": lead_id
        },
        "product_info": {
            "name": product_name,
            "description": "A versatile set of fashion accessories that transform any outfit",
            "goals": "Increase brand awareness and drive product interest",
            "target_audience": "18-34 year old fashion-forward consumers",
            "key_messages": f"1. {product_name} is unique and high-quality\n2. It enhances personal style\n3. It's versatile and easy to use"
        }
    }

    # Find the generate_script_concepts task
    script_task = None
    for task in crew_instance.tasks:
        if task.config.get("description", "").startswith("Analyze the creator's MongoDB data"):
            script_task = task
            break

    if not script_task:
        print("Error: Script generation task not found!")
        sys.exit(1)

    # Find the script_generator agent
    script_agent = None
    for agent in crew_instance.agents:
        if agent.role == "Creative Script Intelligence Specialist":
            script_agent = agent
            break

    if not script_agent:
        print("Error: Script generator agent not found!")
        sys.exit(1)

    # Execute just the script generation task
    result = script_agent.execute_task(
        script_task,
        context="",
        inputs=inputs
    )

    print("\n\n==== GENERATED SCRIPT CONCEPTS ====\n")
    print(result)


if __name__ == "__main__":
    main()
