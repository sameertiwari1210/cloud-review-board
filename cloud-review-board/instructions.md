# Cloud Security Review Board (CSRB) Agent — Unified Instructions

Welcome to the CSRB Agent project! This project is a local-first, first-principles Agentic AI learning project designed to simulate a real Cloud Architecture Review Board. We will build this together step-by-step, strictly following the development methodology to ensure complete understanding of Agentic AI.

---

## 🛠️ Technology Stack & Rules
* **Language**: Python 3.12+ (Only Python Standard Library, SQLite, `openai`, and `python-dotenv`).
* **No Frameworks**: Do **NOT** use LangChain, LangGraph, CrewAI, AutoGen, Pydantic AI, LlamaIndex, or OpenAI Agents SDK.
* **Keep it Simple**: Prefer simple functions over complex classes. Limit functions to a maximum of **50 lines** each.
* **Understandable**: Code must be beginner-friendly and educational. Explain *why* a function exists, *what* it receives, and *what* it returns.
* **Verbose**: Print intermediate outputs and token/execution timestamps to visualize agent flow.

---

## 📈 Step-by-Step Development Phases

We will implement exactly **one phase at a time**. After each phase, we must:
1. Run the application.
2. Verify functionality.
3. Fix any bugs.
4. Update the `README.md` (include Architecture Diagram, Learning Notes, Manual Testing Steps, and Example Output).
5. Commit to Git (e.g., `git commit -m "Phase X - Description"`).
6. Stop and request user approval before starting the next phase.

### Phase 1: Foundation & Single Agent (Architect)
* **Goal**: Build a simple project structure and get a single Architect Agent responding to cloud questions.
* **Project Structure**:
  ```
  project/
  ├── main.py
  ├── llm.py
  ├── prompts.py
  ├── agents/
  │   ├── architect.py
  │   ├── security.py
  │   ├── finops.py
  │   ├── sre.py
  │   └── judge.py
  ├── data/
  └── README.md
  ```
* **Architect Agent**: Creates the cloud architecture based on the user request.
* **Output Section**: Architecture Overview, Components, Security Controls.

### Phase 2: Conversation Memory
* **Goal**: Enable the system to remember user preferences across questions.
* **Create**: `data/memory.json` and `memory.py`.
* **Functions**: `save_memory()`, `load_memory()`, `update_memory()`.
* **Details**: Store cloud preferences (AWS, Azure, GCP, Kubernetes, Terraform, etc.) and pass memory context to agents.

### Phase 3: Add Static Tools
* **Goal**: Create mock tools to analyze files without connecting to the internet.
* **Create**: `tools/terraform_tool.py`, `tools/kubernetes_tool.py`, `tools/aws_tool.py`, `tools/architecture_tool.py`.
* **Terraform Tool**: Check for `0.0.0.0/0`, missing encryption, missing tags, public resources.
* **Kubernetes Tool**: Check for `latest` tags, privileged containers, `hostPath`, missing resource limits.
* **AWS Tool**: Look up Well-Architected and security best practices from static files.

### Phase 4: Tool Routing Agent
* **Goal**: Add a keyword-based tool router.
* **Create**: `tool_router.py`.
* **Details**: Detects if Terraform, Kubernetes, or AWS tools should run (e.g. if the user prompt has "terraform", run the Terraform tool).

### Phase 5: Multi-Agent Architecture Review Board
* **Goal**: Chain the agents in a sequential pipeline.
* **Pipeline**: User Prompt → Architect → Security → FinOps → SRE → Judge.
* **Details**: Save outputs to disk, display each step separately, and print timestamps for each agent execution.

### Phase 6: SQLite Persistence
* **Goal**: Replace the JSON memory with SQLite.
* **Create**: `database.py`.
* **Tables**: `conversations`, `agent_outputs`, `user_preferences`.
* **Details**: Persist every run and allow replaying previous sessions.

### Phase 7: Local RAG (Retrieval-Augmented Generation)
* **Goal**: Enable agents to query local documents without external databases.
* **Create**: `knowledge/` containing markdown or text files (AWS Well-Architected, CIS benchmarks, Kubernetes best practices, Palo Alto practices).
* **Create**: `document_loader.py`.
* **Details**: Load files, chunk text, store chunks in SQLite. Implement keyword search (no vector database) for retrieval context.

### Phase 8: Evaluation Agent
* **Goal**: Add a self-correcting evaluation loop.
* **Create**: `evaluator.py`.
* **Details**: Evaluation Agent scores Architect's output (1-10) for accuracy, completeness, and security. If score < 7, send back to the Architect to regenerate. Limit retries to 2.

### Phase 9: Interactive CLI
* **Goal**: Build a simple command-line interface.
* **Menu Options**:
  1. Ask Architecture Question
  2. Review Terraform Code
  3. Review Kubernetes Manifests
  4. Show Current Memory
  5. Show Conversation History
  6. Exit
* **Details**: Use standard Python `input()` and keep it terminal-based.

### Phase 10: Prepare for LangGraph
* **Goal**: Document how our manual state machine maps to standard frameworks.
* **Create**: `docs/langgraph_mapping.md`.
* **Details**: Map nodes, tools, state, and edge routing to LangGraph equivalents to show understanding.

---

## 🎯 Acceptance & Success Criteria
For **each** phase, before writing code, we must specify:
1. **Definition of Success**: What does a working implementation look like?
2. **Test Cases**: How will we test it?
3. **Expected Output**: What text, files, or print logs should we see?

---

## 🐛 Debugging Protocol
When an error occurs, we must:
1. Explain the error and stack trace.
2. Explain the root cause.
3. Detail the fix.
4. Apply the fix and update docs/comments as needed.

---

## ✍️ Code Comments & Documentation
Every function must be preceded by a comment blocks explaining:
```python
# Why: [Explanation of why this function exists]
# Inputs: [Parameter types and descriptions]
# Outputs: [Return value types and descriptions]
```
