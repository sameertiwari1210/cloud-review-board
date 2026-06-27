# ==============================================================================
# Judge Agent — Full Implementation (Phase 5)
# ==============================================================================
from datetime import datetime
from llm import get_llm_response
from prompts import JUDGE_SYSTEM_PROMPT


# Why: Returns a formatted timestamp string for verbose execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Runs the Judge Agent to synthesise all prior agent reviews into a final
#      architecture verdict with a score and a clear PASS/FAIL decision.
# Inputs:
#   - query (str): The original user request.
#   - security_review (str): Output from the Security Agent.
#   - finops_review (str): Output from the FinOps Agent.
#   - sre_review (str): Output from the SRE Agent.
# Outputs:
#   - str: A final verdict with overall score, decision, and top action items.
def run_judge_agent(
    query: str,
    security_review: str,
    finops_review: str,
    sre_review: str
) -> str:
    print(f"[{_ts()}] [Judge Agent] Synthesising all reviews into final verdict...")

    system_message = JUDGE_SYSTEM_PROMPT.format(
        user_query=query,
        security_review=security_review,
        finops_review=finops_review,
        sre_review=sre_review,
        timestamp=datetime.utcnow().isoformat()
    )
    user_message = "Please deliver the final architecture review verdict."
    result = get_llm_response(user_message, system_message=system_message)

    print(f"[{_ts()}] [Judge Agent] Final verdict delivered.")
    return result
