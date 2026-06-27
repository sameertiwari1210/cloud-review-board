# ==============================================================================
# Cloud Security Review Board (CSRB) — main.py
# Phase 9: Interactive CLI with full multi-agent pipeline
# ==============================================================================
# Why: This is the entry point for the CSRB application. It provides an
#      interactive menu-driven CLI that orchestrates the full agent pipeline:
#      Tool Router → Architect (with Evaluator loop) → Security → FinOps → SRE → Judge.
#      All outputs are persisted to SQLite and optionally to JSON memory.
# Inputs: None (interactive via stdin)
# Outputs: Printed agent outputs to stdout; persisted to data/csrb.db.

import sys
import os
from datetime import datetime

# Phase 6: SQLite persistence
from database import init_db, save_conversation, save_agent_output, load_history

# Phase 7: Local RAG
from document_loader import store_chunks, keyword_search

# Phase 4: Tool routing
from tool_router import route_tools

# Agents
from agents.architect import run_architect_agent
from agents.security import run_security_agent
from agents.finops import run_finops_agent
from agents.sre import run_sre_agent
from agents.judge import run_judge_agent

# Phase 8: Evaluator
from evaluator import run_evaluation_loop

# Phase 2: JSON memory (still used for user preferences display)
from memory import load_memory, update_memory


# Why: Returns the current timestamp for execution logging.
# Inputs: None
# Outputs: str — formatted timestamp.
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Why: Prints a string safely on Windows consoles that may not support all Unicode.
# Inputs: text (str) — string to print.
# Outputs: None
def safe_print(text: str) -> None:
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode("utf-8", errors="replace").decode("utf-8"))


# Why: Prints a visual section divider with a label for readability.
# Inputs: label (str) — section title.
# Outputs: None
def print_banner(label: str) -> None:
    width = 60
    print("\n" + "=" * width)
    print(f"  {label}")
    print("=" * width)


# Why: Runs the full multi-agent pipeline for a given user query.
#      Pipeline: Tool Router → Architect (+ Evaluator) → Security → FinOps → SRE → Judge.
# Inputs:
#   - query (str): The user's architecture question.
#   - memory (dict): Current JSON memory for architect context.
# Outputs: None (all outputs printed and persisted to SQLite).
def run_full_pipeline(query: str, memory: dict) -> None:
    ts_start = get_timestamp()
    print(f"\n[{ts_start}] Starting CSRB pipeline for query: '{query[:80]}'")

    # --- Phase 6: Create DB conversation record ---
    conversation_id = save_conversation(query)
    print(f"[DB] Conversation ID: {conversation_id}")

    # --- Phase 7: RAG — retrieve relevant knowledge chunks ---
    print(f"\n[{get_timestamp()}] [RAG] Searching knowledge base...")
    rag_context = keyword_search(query, top_n=3)
    if rag_context:
        print(f"[RAG] Injecting {len(rag_context.split())} words of context into architect prompt.")

    # --- Phase 4: Tool routing ---
    print_banner("TOOL ANALYSIS")
    tool_findings = route_tools(query)
    if tool_findings:
        safe_print(tool_findings)
        save_agent_output(conversation_id, "ToolRouter", tool_findings)
    else:
        print("  No static tool analysis triggered.")

    # --- Phase 8: Architect with Evaluator loop ---
    # Inject RAG context into query if available
    enriched_query = query
    if rag_context:
        enriched_query = f"{query}\n\n{rag_context}"

    def architect_fn(q: str) -> str:
        return run_architect_agent(q, memory)

    print_banner("ARCHITECT DESIGN (with Evaluator)")
    architecture = run_evaluation_loop(enriched_query, architect_fn)
    safe_print(architecture)
    save_agent_output(conversation_id, "Architect", architecture)

    # --- Phase 5: Security Agent ---
    print_banner("SECURITY REVIEW")
    security_review = run_security_agent(query, architecture)
    safe_print(security_review)
    save_agent_output(conversation_id, "Security", security_review)

    # --- Phase 5: FinOps Agent ---
    print_banner("FINOPS REVIEW")
    finops_review = run_finops_agent(query, architecture)
    safe_print(finops_review)
    save_agent_output(conversation_id, "FinOps", finops_review)

    # --- Phase 5: SRE Agent ---
    print_banner("SRE REVIEW")
    sre_review = run_sre_agent(query, architecture)
    safe_print(sre_review)
    save_agent_output(conversation_id, "SRE", sre_review)

    # --- Phase 5: Judge Agent ---
    print_banner("FINAL VERDICT (Judge)")
    verdict = run_judge_agent(query, security_review, finops_review, sre_review)
    safe_print(verdict)
    save_agent_output(conversation_id, "Judge", verdict)

    # --- Phase 2: Persist to JSON memory ---
    update_memory(query, architecture, reviewer_response=security_review)

    ts_end = get_timestamp()
    print(f"\n[{ts_end}] Pipeline complete. Conversation ID: {conversation_id}")


# Why: Handles menu option 2 — allows the user to paste Terraform code
#      and receive a static analysis report.
# Inputs: None (reads from stdin)
# Outputs: None (prints findings)
def handle_terraform_review() -> None:
    print("\nPaste your Terraform code below.")
    print("When done, enter a line with just 'END' and press Enter.\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    code = "\n".join(lines)
    from tools.terraform_tool import run_terraform_analysis
    print_banner("TERRAFORM STATIC ANALYSIS")
    safe_print(run_terraform_analysis(code))


# Why: Handles menu option 3 — allows the user to paste a Kubernetes manifest
#      and receive a security check report.
# Inputs: None (reads from stdin)
# Outputs: None (prints findings)
def handle_k8s_review() -> None:
    print("\nPaste your Kubernetes manifest below.")
    print("When done, enter a line with just 'END' and press Enter.\n")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)
    manifest = "\n".join(lines)
    from tools.kubernetes_tool import run_k8s_check
    print_banner("KUBERNETES STATIC ANALYSIS")
    safe_print(run_k8s_check(manifest))


# Why: Displays the current JSON memory (user preferences and recent discussions).
# Inputs: None
# Outputs: None (prints to stdout)
def handle_show_memory() -> None:
    memory = load_memory()
    print_banner("CURRENT MEMORY")
    prefs = memory.get("user_preferences", {})
    print(f"  Preferred Cloud : {prefs.get('preferred_cloud', 'N/A')}")
    tools = prefs.get("preferred_tools", [])
    print(f"  Preferred Tools : {', '.join(tools) if tools else 'N/A'}")
    discussions = memory.get("previous_discussions", [])
    print(f"  Stored sessions : {len(discussions)}")


# Why: Displays the N most recent conversations stored in SQLite.
# Inputs: None
# Outputs: None (prints to stdout)
def handle_show_history() -> None:
    print_banner("CONVERSATION HISTORY (last 5)")
    history = load_history(limit=5)
    if not history:
        print("  No conversations recorded yet.")
        return
    for conv in history:
        print(f"\n  [{conv['id']}] {conv['started_at']}")
        print(f"  Query: {conv['query'][:100]}")
        agents_run = [o["agent_name"] for o in conv["outputs"]]
        print(f"  Agents: {', '.join(agents_run)}")


# Why: Entry point for the interactive CLI.  Displays the menu loop and
#      delegates to the appropriate handler based on the user's selection.
# Inputs: None
# Outputs: None
def main() -> None:
    # --- Startup initialisation ---
    print("=" * 60)
    print("   Cloud Security Review Board (CSRB) Agent — Phase 9")
    print("=" * 60)

    # Phase 6: ensure DB tables exist
    init_db()

    # Phase 7: index knowledge documents into SQLite
    print(f"\n[{get_timestamp()}] [RAG] Indexing knowledge base...")
    store_chunks()

    # Phase 2: load memory for context display
    memory = load_memory()
    prefs = memory.get("user_preferences", {})
    print(f"\n[Context] Cloud: {prefs.get('preferred_cloud', 'N/A')} | "
          f"Tools: {', '.join(prefs.get('preferred_tools', [])) or 'N/A'}")

    # --- Interactive menu loop ---
    while True:
        print("\n" + "-" * 40)
        print("  CSRB Main Menu")
        print("-" * 40)
        print("  1. Ask Architecture Question")
        print("  2. Review Terraform Code")
        print("  3. Review Kubernetes Manifests")
        print("  4. Show Current Memory")
        print("  5. Show Conversation History")
        print("  6. Exit")
        print("-" * 40)

        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            query = input("\nEnter your cloud architecture question: ").strip()
            if not query:
                print("ERROR: Question cannot be empty.")
                continue
            run_full_pipeline(query, memory)
            # Reload memory so next question sees updated discussions
            memory = load_memory()

        elif choice == "2":
            handle_terraform_review()

        elif choice == "3":
            handle_k8s_review()

        elif choice == "4":
            handle_show_memory()

        elif choice == "5":
            handle_show_history()

        elif choice == "6":
            print("\nGoodbye! Thank you for using CSRB.")
            sys.exit(0)

        else:
            print("Invalid option. Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()
