# ==============================================================================
# Security Agent — Full Implementation (Phase 5)
# ==============================================================================
from datetime import datetime
from llm import get_llm_response
from prompts import SECURITY_REVIEWER_SYSTEM_PROMPT


# Why: Returns a formatted timestamp string for verbose execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Runs the Security Agent to review the Architect's output for security
#      weaknesses, missing controls, and compliance concerns.
# Inputs:
#   - query (str): The original user request.
#   - architecture (str): The Architect Agent's full output.
# Outputs:
#   - str: A structured security review covering Executive Summary,
#          Security Controls, and Recommendations.
def run_security_agent(query: str, architecture: str) -> str:
    print(f"[{_ts()}] [Security Agent] Starting security review of architecture...")

    system_message = SECURITY_REVIEWER_SYSTEM_PROMPT.format(
        user_query=query,
        architecture=architecture,
        timestamp=datetime.utcnow().isoformat()
    )
    user_message = "Please review the architecture above for security concerns."
    result = get_llm_response(user_message, system_message=system_message)

    print(f"[{_ts()}] [Security Agent] Security review complete.")
    return result
