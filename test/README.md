# test
Implement test time compute using an agentic framework to emulate o1 with Claude.

## How to build your Crew Agent
### With the CLI
Add an agent using AgentStack with the CLI:  
`agentstack generate agent <agent_name>`  
You can also shorten this to `agentstack g a <agent_name>`  
For wizard support use `agentstack g a <agent_name> --wizard`  
Finally for creation in the CLI alone, use `agentstack g a <agent_name> --role/-r <role> --goal/-g <goal> --backstory/-b <backstory> --model/-m <provider/model>`

This will automatically create a new agent in the `agents.yaml` config as well as in your code. Either placeholder strings will be used, or data included in the wizard.

Similarly, tasks can be created with `agentstack g t <tool_name>`

Add tools with `agentstack tools add` and view tools available with `agentstack tools list`

## How to use your Agent
In this directory, run `uv pip install --requirements pyproject.toml`

To run your project, use the following command:  
`agentstack run`

This will initialize your crew of AI agents and begin task execution as defined in your configuration in the main.py file.

#### Replay Tasks from Latest Crew Kickoff:

CrewAI now includes a replay feature that allows you to list the tasks from the last run and replay from a specific one. To use this feature, run:  
`crewai replay <task_id>`  
Replace <task_id> with the ID of the task you want to replay.

#### Reset Crew Memory
If you need to reset the memory of your crew before running it again, you can do so by calling the reset memory feature:  
`crewai reset-memory`  
This will clear the crew's memory, allowing for a fresh start.

> 🪩 Project built with [AgentStack](https://github.com/AgentOps-AI/AgentStack)

# Artik Creative Script Intelligence Agent

This project implements an AI-powered script generation agent for Artik, capable of analyzing creator content and generating tailored video script concepts based on lead data from MongoDB.

## Features

- **Creator Data Analysis**: Fetches and analyzes creator data from MongoDB
- **Video Analysis**: Captures and analyzes screenshots from TikTok videos
- **Script Generation**: Generates customized video script concepts based on creator style and brand requirements

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Set up environment variables (create a `.env` file):

```
OPENAI_API_KEY=your_openai_api_key
MONGODB_URI=your_mongodb_connection_string
```

## Usage

### Using the Agent Directly

You can use the script generator agent directly by running the example script:

```bash
python src/examples/generate_scripts.py <lead_id> <product_name> <product_description> [campaign_goals] [target_audience]
```

Example:

```bash
python src/examples/generate_scripts.py 67d109795a08effb5160dcf0 "StyleBoost Accessory Set" "A versatile set of fashion accessories that transform any outfit"
```

### Using the CrewAI Framework

This agent is set up to work with the CrewAI framework. To run the agent with the full crew:

```bash
python src/main.py
```

You will need to provide input in the `src/config/inputs.yaml` file:

```yaml
query: "Generate video script concepts for lead 67d109795a08effb5160dcf0 and product 'StyleBoost Accessory Set'"
lead_data: 
  id: "67d109795a08effb5160dcf0"
product_info:
  name: "StyleBoost Accessory Set"
  description: "A versatile set of fashion accessories that transform any outfit"
  goals: "Increase brand awareness and drive product interest"
  target_audience: "18-34 year old fashion-forward consumers"
  key_messages: "1. StyleBoost is unique and high-quality\n2. It enhances personal style\n3. It's versatile and easy to use"
```

## How It Works

The script generator agent:

1. **Retrieves lead data** from MongoDB using the provided lead ID
2. **Analyzes top-performing videos** to identify what drives engagement
3. **Captures screenshots** from the creator's highest-performing TikTok videos
4. **Analyzes the visual style** using computer vision AI
5. **Generates 3-5 script concepts** tailored to the creator's style and product requirements

Each script concept includes:
- A compelling hook
- Shot-by-shot breakdown with timing
- Text overlay recommendations
- Music/sound suggestions
- Caption strategy with hashtags

## Agent Architecture

The system consists of several components:

- **MongoDB Client Tool**: Fetches and processes lead data
- **TikTok Video Analyzer Tool**: Captures and analyzes video screenshots
- **Script Generator Tool**: Creates tailored script concepts
- **Script Generator Agent**: Orchestrates the process and provides expert reasoning

## Example Output

```
==== GENERATED SCRIPT CONCEPTS ====

# Concept 1: "Style Transformation Challenge with StyleBoost"

## Hook
"Watch how ONE accessory completely transforms this basic outfit..."

## Shot-by-Shot Breakdown
1. Opening (0:00-0:03): Drew in simple base outfit looking unimpressed
2. Discovery (0:03-0:06): Drew unboxing StyleBoost, close-up of product
3. Styling (0:06-0:12): Quick cuts of Drew trying different styling options
4. Reveal (0:12-0:18): Full outfit transformation with StyleBoost as focal point
5. Details (0:18-0:22): Close-ups of how StyleBoost elevates the look
6. Call-to-Action (0:22-0:24): Drew asking viewers which styling they prefer

## Text Overlays
- "Basic fit 😐" (0:02)
- "StyleBoost transform ✨" (0:10)
- "Which look would YOU wear?" (0:22)

## Music
Upbeat, fashion-forward track with clear beat transitions

## Caption
"When your intuition says 'try something new' but you're not sure... StyleBoost is that missing piece that transforms EVERYTHING! Which styling would you rock? #styleinspo #outfitideas #StyleBoost #transformation"

(Additional concepts would follow...)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms of the LICENSE file included in the repository.