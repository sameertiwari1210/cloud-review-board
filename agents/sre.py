# ==============================================================================
# SRE Agent — Full Implementation (Phase 5)
# ==============================================================================
from datetime import datetime
from llm import get_llm_response
from prompts import SRE_SYSTEM_PROMPT


# Why: Returns a formatted timestamp string for verbose execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Runs the SRE Agent to review the architecture for reliability,
#      observability, SLO definition, and incident response readiness.
# Inputs:
#   - query (str): The original user request.
#   - architecture (str): The Architect Agent's full output.
# Outputs:
#   - str: An SRE review covering reliability concerns and recommendations.
def run_sre_agent(query: str, architecture: str) -> str:
    print(f"[{_ts()}] [SRE Agent] Starting reliability and observability review...")

    system_message = SRE_SYSTEM_PROMPT.format(
        user_query=query,
        architecture=architecture,
        timestamp=datetime.utcnow().isoformat()
    )
    user_message = "Please review the architecture above for reliability, observability, and SRE concerns."
    result = get_llm_response(user_message, system_message=system_message)

    print(f"[{_ts()}] [SRE Agent] SRE review complete.")
    return result
