from datetime import datetime
from llm import get_llm_response
from prompts import ARCHITECT_SYSTEM_PROMPT

# Why: Simple helper to generate current timestamp for tracking agent executions.
# Inputs: None
# Outputs: Current timestamp formatted as string.
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Why: Runs the Cloud Architect Agent to generate a cloud architecture design.
# Inputs:
#   - query (str): The user's cloud architecture question.
# Outputs:
#   - str: The generated architecture design proposal.
def run_architect_agent(query: str) -> str:
    timestamp = get_timestamp()
    print(f"[{timestamp}] [Architect Agent] Starting architectural design for query: '{query}'")
    
    # Send user request to LLM with the custom Architect instructions
    design = get_llm_response(query, system_message=ARCHITECT_SYSTEM_PROMPT)
    
    timestamp_done = get_timestamp()
    print(f"[{timestamp_done}] [Architect Agent] Architecture proposal successfully created.")
    
    return design
