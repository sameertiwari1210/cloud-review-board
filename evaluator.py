# ==============================================================================
# Evaluator — Phase 8: Self-Correcting Evaluation Loop
# ==============================================================================
# Why: Adds a quality gate between the Architect and the rest of the pipeline.
#      If the Architect produces a low-quality response (score < 7 out of 10),
#      the output is sent back with feedback for regeneration (max 2 retries).

import re
from datetime import datetime
from llm import get_llm_response
from prompts import EVALUATOR_SYSTEM_PROMPT

# Minimum acceptable score before passing the output downstream.
PASS_THRESHOLD = 7

# Maximum number of regeneration attempts after an initial failure.
MAX_RETRIES = 2


# Why: Returns a formatted timestamp string for verbose execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Asks the LLM to score an architecture design and return structured feedback.
# Inputs:
#   - query (str): The original user request.
#   - architecture (str): The Architect's output to evaluate.
# Outputs:
#   - tuple[int, str]: (score, feedback) where score is 1-10 and feedback is text.
def evaluate_architecture(query: str, architecture: str) -> tuple:
    print(f"[{_ts()}] [Evaluator] Scoring architecture output...")

    system_message = EVALUATOR_SYSTEM_PROMPT.format(
        user_query=query,
        architecture=architecture
    )
    user_message = "Please evaluate the architecture design above."
    raw = get_llm_response(user_message, system_message=system_message)

    # Parse SCORE and FEEDBACK from the response
    score = _parse_score(raw)
    feedback = _parse_feedback(raw)

    print(f"[{_ts()}] [Evaluator] Score: {score}/10")
    print(f"[{_ts()}] [Evaluator] Feedback: {feedback[:120]}...")
    return score, feedback


# Why: Extracts the integer score from the evaluator's raw output.
# Inputs:
#   - raw (str): The full evaluator response text.
# Outputs:
#   - int: Parsed score (defaults to 5 if parsing fails).
def _parse_score(raw: str) -> int:
    match = re.search(r"SCORE:\s*(\d+)", raw, re.IGNORECASE)
    if match:
        return min(10, max(1, int(match.group(1))))
    # Fallback: look for standalone digit at start of line
    match = re.search(r"^\s*(\d+)\s*[/\\]?\s*10", raw, re.MULTILINE)
    if match:
        return min(10, max(1, int(match.group(1))))
    return 5  # safe default if parsing fails


# Why: Extracts the feedback text from the evaluator's raw output.
# Inputs:
#   - raw (str): The full evaluator response text.
# Outputs:
#   - str: Parsed feedback paragraph.
def _parse_feedback(raw: str) -> str:
    match = re.search(r"FEEDBACK:\s*(.+)", raw, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw.strip()


# Why: Wraps the Architect agent in an evaluation loop.  If the score is below
#      the threshold, it regenerates the design with the evaluator's feedback
#      injected into the prompt as an improvement hint.
# Inputs:
#   - query (str): The original user request.
#   - architect_fn (callable): A function that accepts (query: str) -> str.
# Outputs:
#   - str: The highest-quality architecture design produced within the retry limit.
def run_evaluation_loop(query: str, architect_fn) -> str:
    attempt = 0
    current_query = query

    while attempt <= MAX_RETRIES:
        attempt_label = "Initial" if attempt == 0 else f"Retry {attempt}"
        print(f"\n[{_ts()}] [Evaluator] {attempt_label} architecture generation...")

        design = architect_fn(current_query)
        score, feedback = evaluate_architecture(query, design)

        if score >= PASS_THRESHOLD:
            print(f"[{_ts()}] [Evaluator] Score {score}/10 meets threshold ({PASS_THRESHOLD}). Passing output.")
            return design

        if attempt >= MAX_RETRIES:
            print(f"[{_ts()}] [Evaluator] Max retries reached. Using best available output (score {score}/10).")
            return design

        # Augment the query with evaluator feedback for the next attempt
        print(f"[{_ts()}] [Evaluator] Score {score}/10 below threshold. Regenerating with feedback...")
        current_query = (
            f"{query}\n\n"
            f"[Improvement Required — Previous Score: {score}/10]\n"
            f"{feedback}\n"
            f"Please address the above feedback and produce an improved response."
        )
        attempt += 1

    return design  # fallback (unreachable but satisfies linters)
