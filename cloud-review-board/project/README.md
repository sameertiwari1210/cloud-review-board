# CSRB — Phase 1: Foundation & Single Architect Agent

This is the first phase of the Cloud Security Review Board (CSRB) Agent project. In this phase, we establish our foundation, setup our python environment using `uv`, and implement the very first agent: the **Architect Agent**.

---

## 🏗️ Architecture Diagram

Here is a visual breakdown of how Phase 1 functions:

```
+-------------------------------------------------------------+
|                        USER INPUT                           |
|  "Design secure AWS hub-and-spoke TGW Palo Alto firewall"  |
+-------------------------------------------------------------+
                               │
                               ▼
+-------------------------------------------------------------+
|                  project/main.py (CLI core)                 |
|  - Parses argument/prompt input                            |
|  - Verifies workspace configs                               |
+-------------------------------------------------------------+
                               │
                               ▼
+-------------------------------------------------------------+
|             project/agents/architect.py (Agent)             |
|  - Implements run_architect_agent(query)                   |
|  - Injects system prompts and runs completions              |
+-------------------------------------------------------------+
                               │
                               ▼
+-------------------------------------------------------------+
|                  project/llm.py (API Layer)                 |
|  - Loads environment configurations (.env)                  |
|  - Connects to OpenAI, LM Studio, or Ollama via OpenAI SDK |
+-------------------------------------------------------------+
                               │
                               ▼
+-------------------------------------------------------------+
|                 API Endpoints / Local LLM                   |
|  - OpenAI Cloud (gpt-4o-mini)                               |
|  - LM Studio (http://localhost:1234)                        |
|  - Ollama (http://localhost:11434)                          |
+-------------------------------------------------------------+
```

---

## 🛠️ Setup Instructions

This project is built using **Python 3.12+** and is managed with the ultra-fast package manager **uv**.

### 1. Configure the Environment
Create a copy of `.env.template` named `.env` inside the `project/` directory:
```bash
cp .env.template .env
```
Open `.env` and fill in your details:
* **For OpenAI Cloud**: Insert your `OPENAI_API_KEY`.
* **For LM Studio**: Uncomment `OPENAI_API_BASE=http://localhost:1234/v1` and add a dummy key.
* **For Ollama**: Uncomment `OPENAI_API_BASE=http://localhost:11434/v1` and set `OPENAI_MODEL` to your downloaded model name (e.g. `llama3`).

### 2. Run the Agent
Run the project using `uv` from the `project/` directory:
```bash
uv run python main.py "Design a secure AWS hub-and-spoke network using Transit Gateway and Palo Alto firewalls."
```

Alternatively, you can run the program interactively:
```bash
uv run python main.py
```

---

## 🧠 Learning Notes

In this phase, we learned:
1. **First-Principles Agent Setup**: How to design an agent using simple prompt structures without frameworks.
2. **OpenAI Compatibility**: How to configure standard OpenAI SDK to talk to local providers (Ollama / LM Studio) by simply updating the `base_url`.
3. **Structured Prompts**: By setting strict system instructions, we can force the model to output reliable markdown with custom headers.

---

## 🧪 Manual Verification Steps

1. Run the app without arguments and type a prompt when asked:
   ```bash
   uv run python main.py
   ```
2. Verify that:
   * Execution logs with timestamps are displayed.
   * The debug print shows the active model/endpoint.
   * The final output displays three clear sections: `# Architecture Overview`, `# Components`, and `# Security Controls`.
