import os
import json

# Why: Defines a reliable relative path for the memory file so it resolves
#      correctly regardless of where the terminal session was launched.
# Inputs: None
# Outputs: Absolute file path string.
MEMORY_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "memory.json")

# Why: Provides a clean starter profile if no memory file exists.
# Inputs: None
# Outputs: Dictionary of default preferences and discussions.
def get_default_memory() -> dict:
    return {
        "user_preferences": {
            "preferred_cloud": "AWS",
            "preferred_tools": ["Terraform"]
        },
        "previous_discussions": []
    }

# Why: Loads memory from the local JSON file. If the file or the data folder
#      doesn't exist, it creates them with default configurations.
# Inputs: None
# Outputs: Dictionary containing the parsed memory data.
def load_memory() -> dict:
    # If the file does not exist, initialize it with default values
    if not os.path.exists(MEMORY_FILE_PATH):
        # Ensure the parent directory (project/data) exists
        os.makedirs(os.path.dirname(MEMORY_FILE_PATH), exist_ok=True)
        default_mem = get_default_memory()
        save_memory(default_mem)
        return default_mem
        
    try:
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"WARNING: Failed to load memory.json ({e}). Resetting to defaults.")
        return get_default_memory()

# Why: Writes the updated memory dictionary back to the JSON file.
# Inputs: 
#   - memory_data (dict): The memory dictionary to write.
# Outputs: None
def save_memory(memory_data: dict) -> None:
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(MEMORY_FILE_PATH), exist_ok=True)
        with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
            # indent=4 writes formatted, readable json for easier user inspection
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"ERROR: Failed to save memory to {MEMORY_FILE_PATH}. Exception: {e}")

# Why: Appends a new conversation thread to the discussion history in memory.
# Inputs:
#   - query (str): The architectural question submitted by the user.
#   - response (str): The final recommendation output by the agent system.
# Outputs: None
def update_memory(query: str, response: str, reviewer_response: str | None = None) -> None:
    memory = load_memory()
    
    # Store the conversation thread as a structured log
    new_discussion = {
        "query": query,
        "architect_response": response
    }
    if reviewer_response is not None:
        new_discussion["reviewer_response"] = reviewer_response
    
    memory["previous_discussions"].append(new_discussion)
    save_memory(memory)
