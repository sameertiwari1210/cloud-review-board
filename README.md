# 🛡️ Cloud Security Review Board (CSRB) Agent

> **A first-principles Agentic AI learning project — no frameworks, no magic, just Python.**

Built with **Python 3.12+** and exactly **two third-party packages**: `openai` and `python-dotenv`.
No LangChain. No LangGraph. No CrewAI. No AutoGen. Every concept is implemented from scratch so you can see exactly how Agentic AI works under the hood.

---

## 🤔 What Is This?

Imagine a real Cloud Architecture Review Board — a panel of expert engineers who review cloud designs for security, cost, and reliability. This project simulates that board as a **multi-agent AI pipeline**.

You describe a cloud architecture (or paste Terraform/Kubernetes code), and a team of AI agents:
1. **Architect Agent** — designs the solution
2. **Evaluator** — scores the design and retries if quality is low
3. **Security Agent** — reviews for security vulnerabilities
4. **FinOps Agent** — reviews for cost efficiency
5. **SRE Agent** — reviews for reliability and operations
6. **Judge Agent** — synthesises all reviews into a final verdict

**Who is this for?**
- Developers learning how AI agents work from scratch
- Cloud engineers who want to see AI applied to architecture reviews
- Anyone curious about building LLM pipelines without a framework

---

## 🧠 AI Concepts You Will Learn

| Concept | What It Means | Where in This Project |
|---|---|---|
| **Agent** | An LLM + a prompt + optional tools | Every file in `agents/` |
| **Multi-Agent Pipeline** | Chaining agents so each builds on the last | `run_full_pipeline()` in `main.py` |
| **Tool Use** | Calling external functions from agent logic | `tool_router.py` → `tools/` |
| **RAG** (Retrieval-Augmented Generation) | Injecting relevant docs into the prompt | `document_loader.py` + `knowledge/` |
| **Self-Correction / Evaluator Loop** | An agent that scores another agent's work | `evaluator.py` |
| **Short-Term Memory** | Remembering the current conversation | `memory.py` (JSON) |
| **Long-Term Memory / Persistence** | Storing all sessions in a database | `database.py` (SQLite) |
| **Human-in-the-Loop** | A human approves/steers the pipeline | Interactive CLI in `main.py` |
| **State Machine** | Sequential steps with conditional branching | `run_full_pipeline()` flow |

---

## 🏗️ Architecture Diagram

Here is the **actual data flow** through the system when you ask an architecture question:

```
User Input (CLI)
      │
      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    main.py  ─  run_full_pipeline()              │
│                                                                 │
│  Step 1 ── Phase 6: SQLite                                      │
│            Save new conversation record to csrb.db             │
│                  │                                              │
│  Step 2 ── Phase 7: RAG (document_loader.py)                    │
│            Keyword-search knowledge/*.md files in SQLite        │
│            Inject top-3 matching chunks into the architect's    │
│            prompt as contextual knowledge                       │
│                  │                                              │
│  Step 3 ── Phase 4: Tool Router (tool_router.py)                │
│            Detect keywords → run matching static tool           │
│            ┌─────────────────────────────────────────────────┐ │
│            │  "terraform"/"hcl" → terraform_tool.py          │ │
│            │  "kubernetes"/"k8s" → kubernetes_tool.py        │ │
│            │  "aws"/"vpc"/"s3"  → aws_tool.py                │ │
│            └─────────────────────────────────────────────────┘ │
│            Tool findings printed and saved to DB                │
│                  │                                              │
│  Step 4 ── Phase 8: Evaluator Loop (evaluator.py)               │
│            ┌─────────────────────────────────────────────────┐ │
│            │  Architect Agent generates design               │ │
│            │        │                                        │ │
│            │  Evaluator scores it (accuracy/completeness/    │ │
│            │  security) on a 1-10 scale                      │ │
│            │        │                                        │ │
│            │  score ≥ 7? ──YES──► pass to pipeline           │ │
│            │        │                                        │ │
│            │       NO                                        │ │
│            │        └──► inject feedback, retry (max ×2)    │ │
│            └─────────────────────────────────────────────────┘ │
│                  │                                              │
│  Step 5 ── Phase 5: Multi-Agent Review Pipeline                 │
│            ┌─────────────────────────────────────────────────┐ │
│            │  Security Agent  ← receives architect design    │ │
│            │  FinOps Agent    ← receives architect design    │ │
│            │  SRE Agent       ← receives architect design    │ │
│            │       │                                         │ │
│            │  Judge Agent ← receives all three reviews       │ │
│            │       │                                         │ │
│            │  Final Verdict: Score X/10, PASS / FAIL        │ │
│            └─────────────────────────────────────────────────┘ │
│                  │                                              │
│  Step 6 ── Phase 6: Persist all agent outputs to SQLite         │
│            Phase 2: Update JSON memory with preferences         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Repository Layout

```
project/
├── main.py               # Phase 9 — Interactive CLI entry point & pipeline orchestrator
├── llm.py                # LLM client wrapper (OpenAI-compatible; works with any provider)
├── prompts.py            # All system prompt templates for every agent
├── memory.py             # Phase 2 — Short-term JSON-based conversation memory
├── database.py           # Phase 6 — SQLite long-term persistence layer
├── tool_router.py        # Phase 4 — Keyword-based tool dispatcher
├── document_loader.py    # Phase 7 — Local RAG: loads, chunks, and searches knowledge docs
├── evaluator.py          # Phase 8 — Self-correcting evaluation loop (scores + retries)
│
├── agents/
│   ├── architect.py      # Phase 1 — Architect Agent (generates the cloud design)
│   ├── security.py       # Phase 5 — Security Reviewer Agent
│   ├── finops.py         # Phase 5 — FinOps (Cost) Agent
│   ├── sre.py            # Phase 5 — SRE (Reliability) Agent
│   └── judge.py          # Phase 5 — Judge Agent (final verdict)
│
├── tools/
│   ├── terraform_tool.py    # Phase 3 — Terraform static analyser (no LLM)
│   ├── kubernetes_tool.py   # Phase 3 — Kubernetes manifest checker (no LLM)
│   ├── aws_tool.py          # Phase 3 — AWS config security checker
│   └── architecture_tool.py # Phase 3 — Text-based architecture pattern analyser
│
├── knowledge/            # Phase 7 — Local knowledge base (markdown files)
│   ├── aws_well_architected.md
│   ├── cis_benchmarks.md
│   ├── kubernetes_best_practices.md
│   └── palo_alto_practices.md
│
├── docs/
│   └── langgraph_mapping.md  # Phase 10 — Maps this project to LangGraph concepts
│
├── data/                 # Auto-created at runtime (excluded from git)
│   ├── memory.json       # Phase 2 — JSON memory store (auto-created)
│   └── csrb.db           # Phase 6 — SQLite database (auto-created)
│
├── .env.template         # Environment configuration template — copy to .env
├── pyproject.toml        # Project metadata and dependency declarations
└── README.md             # This file
```

---

## 🚀 Setup: Step-by-Step for Beginners

> **Prerequisite**: Python 3.12 or newer. Check with `python --version`.
> If you don't have Python, download it from [python.org](https://www.python.org/downloads/).

### Step 1 — Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/cloud-review-board.git
cd cloud-review-board
```

### Step 2 — Create a virtual environment & install dependencies

Choose **one** of the two options below. Both work fine — pick whichever you prefer.

---

#### Option A — Plain `pip` (simplest, no extra tools needed)

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\activate
pip install openai python-dotenv
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install openai python-dotenv
```

> ✅ **How do I know the venv is active?** Your terminal prompt will show `(.venv)` at the start.
>
> Only two packages are installed — `openai` (to talk to any LLM) and `python-dotenv` (to read your `.env` file). No frameworks, no heavy dependencies.

---

#### Option B — `uv` (faster installs, exact reproducible versions)

> **What is `uv`?** It is a fast Python package manager — think of it as a faster replacement for `pip + venv` combined. The project includes a `uv.lock` file which pins the exact version of every package so everyone gets identical installs.
>
> You only need this if you want 100% reproducible installs. If you just want to run the project, use Option A.

Install `uv` (one-time):

```bash
# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then create the environment and install everything in one command:

```bash
uv sync
```

Activate the environment:

```powershell
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

> `uv sync` reads `pyproject.toml` and `uv.lock` and installs the exact same versions used during development. No extra configuration needed.

---

### Step 3 — Configure your LLM provider

Copy the template to create your personal config file:

**Windows:**
```powershell
copy .env.template .env
```

**macOS / Linux:**
```bash
cp .env.template .env
```

Now open `.env` in any text editor and **uncomment one provider block**.

#### 🆓 Free / Low-Cost Provider Options

| Provider | Free Tier? | Sign-Up Link | Model to Use |
|---|---|---|---|
| **Groq** (fastest, recommended for beginners) | ✅ Yes | [console.groq.com](https://console.groq.com/) | `llama-3.3-70b-versatile` |
| **Google Gemini** | ✅ Yes | [aistudio.google.com](https://aistudio.google.com/) | `gemini-2.0-flash` |
| **OpenRouter** | ✅ Free credits | [openrouter.ai](https://openrouter.ai/) | `meta-llama/llama-3.1-8b-instruct:free` |
| **OpenAI** | 💳 Paid | [platform.openai.com](https://platform.openai.com/) | `gpt-4o-mini` |
| **Ollama** (fully local) | ✅ Free | [ollama.com](https://ollama.com/) | `llama3` |
| **LM Studio** (local GUI) | ✅ Free | [lmstudio.ai](https://lmstudio.ai/) | any local model |

#### Example `.env` for Groq (recommended for beginners):

```env
OPENAI_API_BASE=https://api.groq.com/openai/v1
OPENAI_API_KEY=gsk_YOUR_GROQ_API_KEY_HERE
OPENAI_MODEL=llama-3.3-70b-versatile
```

#### Example `.env` for Ollama (100% local, no API key needed):

```env
OPENAI_API_BASE=http://localhost:11434/v1
OPENAI_API_KEY=ollama
OPENAI_MODEL=llama3
```

> ⚠️ **Never commit your `.env` file to Git.** It is already in `.gitignore`.

---

## ▶️ Running the Application

Make sure you are in the project folder (the one that contains `main.py`), and that your virtual environment is **activated** (you see `(.venv)` in your prompt):

```bash
python main.py
```

On first run the application will:
1. Create the `data/` directory automatically
2. Initialize the SQLite database (`data/csrb.db`)
3. Index all files in `knowledge/` into the database for RAG search
4. Display the interactive menu

```
============================================================
   Cloud Security Review Board (CSRB) Agent — Phase 9
============================================================

[2026-06-27 18:00:00] [RAG] Indexing knowledge base...

[Context] Cloud: N/A | Tools: N/A

----------------------------------------
  CSRB Main Menu
----------------------------------------
  1. Ask Architecture Question
  2. Review Terraform Code
  3. Review Kubernetes Manifests
  4. Show Current Memory
  5. Show Conversation History
  6. Exit
----------------------------------------
Select an option (1-6):
```

---

## 🧪 Manual Testing — Try These Examples

### ✅ Option 1 — Ask an Architecture Question

```
Select: 1
Question: Design a secure multi-AZ VPC with a Palo Alto NGFW
```

**What happens step by step:**
1. `[RAG]` — searches `knowledge/` files for relevant context (Palo Alto, AWS VPC)
2. `[Tool Router]` — detects "AWS", "VPC" keywords → runs `aws_tool.py`
3. `[Evaluator]` — Architect generates a design, evaluator scores it (e.g. 8/10)
4. If score ≥ 7: passes the design forward. If < 7: sends back with feedback and retries (max 2×)
5. `SECURITY REVIEW` — Security Agent reviews the design
6. `FINOPS REVIEW` — FinOps Agent reviews costs
7. `SRE REVIEW` — SRE Agent reviews reliability
8. `FINAL VERDICT` — Judge synthesises all three reviews into a score and decision

### ✅ Option 2 — Review Terraform Code

```
Select: 2
Paste:
  resource "aws_security_group" "example" {
    ingress { cidr_blocks = ["0.0.0.0/0"] }
  }
END
```

**Expected output:** Warning about open `0.0.0.0/0` ingress (allows traffic from anywhere).

### ✅ Option 3 — Review a Kubernetes Manifest

```
Select: 3
Paste:
  image: nginx:latest
END
```

**Expected output:** Warning about using `latest` tag (unpinned image version is a security risk).

### ✅ Option 4 — Show Memory

Shows the cloud preferences (e.g. AWS) and conversation count learned from your previous sessions.

### ✅ Option 5 — Show History

Lists the last 5 conversations retrieved from the SQLite database, showing which agents ran.

---

## 📚 Phase-by-Phase Learning Guide

Each phase introduces one new AI concept. Read the code for that phase to understand it deeply.

### Phase 1 — Foundation & Architect Agent
**New concept: What is an AI Agent?**

An agent is just: **LLM + a prompt + an input**. Nothing more.

- File: `agents/architect.py`
- The `run_architect_agent()` function builds a system prompt (the "role") and sends the user's query to the LLM.
- The prompt in `prompts.py` (`ARCHITECT_SYSTEM_PROMPT`) tells the LLM to behave like a cloud architect.
- Output format: 8 sections — Executive Summary, Architecture Diagram, Components, Security Controls, High Availability, Operations, Tradeoffs, Recommendations.

### Phase 2 — Conversation Memory
**New concept: How do agents remember things?**

- File: `memory.py`
- Stores user preferences (preferred cloud, tools) and the last 2 conversation snippets in `data/memory.json`.
- `load_memory()`, `save_memory()`, `update_memory()` — three simple functions.
- Memory is injected into the architect's system prompt so it can say "you mentioned you prefer AWS last time."
- **Short-term memory** = JSON file (fast, simple, lost on disk wipe).

### Phase 3 — Static Analysis Tools
**New concept: Tools (deterministic functions the agent can call)**

- Folder: `tools/`
- These are plain Python functions — no LLM involved.
- `terraform_tool.py`: scans text for known bad patterns (`0.0.0.0/0`, missing encryption, etc.)
- `kubernetes_tool.py`: scans manifests for `latest` tags, privileged containers, missing resource limits.
- `aws_tool.py`: checks for open S3 buckets, overly permissive IAM policies, missing CloudTrail.
- **Key insight**: Tools are deterministic. The LLM is probabilistic. Combining both gives you reliability.

### Phase 4 — Tool Routing Agent
**New concept: How does an agent decide which tool to use?**

- File: `tool_router.py`
- Simple keyword matching: if the user prompt contains "terraform" or ".tf", run the Terraform tool.
- No LLM needed for routing — keyword matching is fast and cheap.
- **Real frameworks** (LangChain, LangGraph) do this with vector search or LLM function-calling. We do it with `if/else`.

### Phase 5 — Multi-Agent Pipeline
**New concept: Agents passing outputs to other agents**

- Files: `agents/security.py`, `agents/finops.py`, `agents/sre.py`, `agents/judge.py`
- Pipeline order: **Architect → Security → FinOps → SRE → Judge**
- Each specialist agent receives the Architect's output and provides a focused review.
- The Judge agent receives all three reviews and produces the final verdict.
- **Each agent has a different system prompt** — that's what makes it a "different" agent.

### Phase 6 — SQLite Persistence
**New concept: Long-term memory with a database**

- File: `database.py`
- Three tables: `conversations`, `agent_outputs`, `user_preferences`
- Every run creates a conversation record; every agent output is stored with a timestamp.
- `load_history(limit=5)` retrieves the last N sessions for the CLI history view.
- **Long-term memory** = SQLite (survives restarts, queryable).

### Phase 7 — Local RAG (Retrieval-Augmented Generation)
**New concept: Giving the LLM access to your own documents**

- Files: `document_loader.py` + `knowledge/*.md`
- RAG = load documents → chunk them → search for relevant chunks → inject into prompt.
- Our implementation: keyword overlap search stored in SQLite (no vector database needed).
- When you ask about "Palo Alto firewall", the system finds the `palo_alto_practices.md` chunk and prepends it to the architect's prompt.
- **Real RAG** uses embeddings + vector databases (e.g. Pinecone, Chroma). Ours proves the concept without them.

### Phase 8 — Evaluation Agent (Self-Correction)
**New concept: Agents evaluating and improving other agents**

- File: `evaluator.py`
- `evaluate_architecture(query, design)` → returns `(score, feedback)`
- The LLM scores the architect's output on: accuracy (4pts) + completeness (3pts) + security (3pts) = max 10
- If score < 7: feedback is injected back into the query and the Architect retries (max 2 times).
- **This is the foundation of self-correcting AI systems** — the same pattern used in AlphaCode, Reflexion, etc.

### Phase 9 — Interactive CLI
**New concept: Human-in-the-Loop**

- File: `main.py`
- A `while True` menu loop with 6 options.
- Options 2 & 3 accept multi-line pasted code (terminated with `END`).
- The human decides what to ask, what code to review, and when to exit — they are in control.

### Phase 10 — LangGraph Mapping
**New concept: How do frameworks abstract what we built?**

- File: `docs/langgraph_mapping.md`
- Maps every concept from this project to its LangGraph equivalent.
- After completing this project, you have the mental model to use any framework.

---

## 💡 Example Output

```
============================================================
  ARCHITECT DESIGN (with Evaluator)
============================================================
[2026-06-27 18:00:01] [Evaluator] Initial architecture generation...
DEBUG: Connecting to LLM [Endpoint: https://api.groq.com/openai/v1] [Model: llama-3.3-70b-versatile]
[2026-06-27 18:00:06] [Evaluator] Scoring architecture output...
[2026-06-27 18:00:08] [Evaluator] Score: 8/10
[2026-06-27 18:00:08] [Evaluator] Score 8/10 meets threshold (7). Passing output.

1. Executive Summary
- Multi-AZ VPC with centralized Palo Alto NGFW inspection via Gateway Load Balancer...

============================================================
  SECURITY REVIEW
============================================================
Executive Summary: The proposed architecture demonstrates strong security posture...

============================================================
  FINAL VERDICT (Judge)
============================================================
Overall Score: 8/10
Decision: PASS ✅

Top 5 Action Items:
1. Enable CloudTrail in all regions with log file validation.
2. Implement WAF rules for all internet-facing load balancers.
3. Enforce MFA on all IAM users and roles.
4. Enable VPC Flow Logs for network traffic monitoring.
5. Apply least-privilege IAM policies across all service accounts.

[2026-06-27 18:00:30] Pipeline complete. Conversation ID: 1
```

---

## 🔧 Troubleshooting

### "OPENAI_API_KEY environment variable is not set"
You haven't created your `.env` file yet. Run `copy .env.template .env` (Windows) or `cp .env.template .env` (Mac/Linux) and add your API key.

### "LLM request failed"
- Check your API key is correct in `.env`
- Check you have internet access (or your local model is running for Ollama/LM Studio)
- Check the model name matches what the provider supports

### "ModuleNotFoundError: No module named 'openai'"
Your virtual environment is not activated. Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux).

### "python: can't open file 'main.py': No such file or directory"
You are in the wrong directory. You need to `cd` into the repository folder (the one that contains `main.py`).

### The evaluator keeps retrying
Your model may be producing short responses. Try a larger model (e.g. `llama-3.3-70b` instead of `llama3-8b`).

### "uv: command not found" (if using Option B)
`uv` is not installed. Either install it using the command in the Setup section, or switch to **Option A** (`pip`) — both install exactly the same packages.

### "No module named X" after `uv sync`
Make sure you activated the virtual environment after running `uv sync`. Run `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Mac/Linux) before running `python main.py`.


---

## 🤝 Contributing

Contributions are welcome! This is a learning project, so clarity and educational value are the top priorities.

**Ways to contribute:**
- 📝 Improve code comments and explanations
- 🧪 Add more test case examples to `README.md`
- 📚 Add new knowledge files to `knowledge/`
- 🔧 Add new static analysis tools to `tools/`
- 🐛 Fix bugs and edge cases

**Before contributing**, please read [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the **MIT License** — see the [`LICENSE`](LICENSE) file for details.

---

*Happy building! — CSRB is a learning project demonstrating Agentic AI fundamentals from first principles.*
*Once you understand every line here, you're ready to use LangChain, LangGraph, CrewAI, or any other framework with confidence.*
