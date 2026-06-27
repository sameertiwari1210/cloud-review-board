# ==============================================================================
# FinOps Agent — Full Implementation (Phase 5)
# ==============================================================================
from datetime import datetime
from llm import get_llm_response
from prompts import FINOPS_SYSTEM_PROMPT


# Why: Returns a formatted timestamp string for verbose execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Runs the FinOps Agent to review the architecture for cost efficiency,
#      right-sizing, and savings opportunities.
# Inputs:
#   - query (str): The original user request.
#   - architecture (str): The Architect Agent's full output.
# Outputs:
#   - str: A FinOps review covering cost concerns and recommendations.
def run_finops_agent(query: str, architecture: str) -> str:
    print(f"[{_ts()}] [FinOps Agent] Starting cost efficiency review...")

    system_message = FINOPS_SYSTEM_PROMPT.format(
        user_query=query,
        architecture=architecture,
        timestamp=datetime.utcnow().isoformat()
    )
    user_message = "Please review the architecture above for cost efficiency and FinOps concerns."
    result = get_llm_response(user_message, system_message=system_message)

    print(f"[{_ts()}] [FinOps Agent] FinOps review complete.")
    return result
