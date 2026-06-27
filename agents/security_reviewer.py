from datetime import datetime
from llm import get_llm_response
from prompts import SECURITY_REVIEWER_SYSTEM_PROMPT

def run_security_reviewer(query: str, architecture: str) -> str:
    """Generate a security review for the given architecture.

    Args:
        query: The original user request that triggered the architecture design.
        architecture: The textual architecture output from the Architect.
    Returns:
        A bullet‑point security assessment.
    """
    system_message = SECURITY_REVIEWER_SYSTEM_PROMPT.format(
        user_query=query,
        architecture=architecture,
        timestamp=datetime.utcnow().isoformat()
    )
    user_message = "Please review the architecture above for security concerns."
    return get_llm_response(system_message, user_message)
