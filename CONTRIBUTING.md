# Contributing to CSRB Agent

Thank you for your interest in contributing! This is a **learning project** — the primary goal is educational clarity. Every contribution should make the code easier to understand for beginners.

---

## 📋 Ground Rules

1. **No frameworks** — Do NOT add LangChain, LangGraph, CrewAI, AutoGen, LlamaIndex, or any other agent framework. The whole point of this project is to build everything from scratch.
2. **Keep it simple** — Prefer simple functions over complex classes. Maximum 50 lines per function.
3. **Comment everything** — Every function must have the standard comment block:
   ```python
   # Why: [Explanation of why this function exists]
   # Inputs: [Parameter types and descriptions]
   # Outputs: [Return value types and descriptions]
   ```
4. **No new heavy dependencies** — The only allowed third-party packages are `openai` and `python-dotenv`. Everything else must use the Python standard library.
5. **No secrets** — Never commit API keys, tokens, or credentials. Check your `.env` is in `.gitignore`.

---

## 🚀 How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/YOUR_USERNAME/CSRB.git
cd CSRB/cloud-review-board/project
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install openai python-dotenv
```

### 3. Create a Branch

Use a descriptive branch name:

```bash
git checkout -b feature/add-azure-tool
git checkout -b fix/evaluator-score-parsing
git checkout -b docs/improve-phase3-explanation
```

### 4. Make Your Changes

- Follow the code style in existing files (standard Python, no type stubs, clear docstrings)
- Add or update the relevant section in `README.md` if your change affects usage
- Test your change manually using the CLI

### 5. Open a Pull Request

Push your branch and open a PR against `main`. In the PR description, include:
- **What** you changed
- **Why** it improves the project (especially: does it make concepts clearer?)
- **How to test it** (what CLI option to use, what input to paste)

---

## 💡 Good First Contributions

| Area | Idea |
|---|---|
| `knowledge/` | Add a new best-practices file (e.g. `azure_security.md`, `gcp_well_architected.md`) |
| `tools/` | Add an Azure or GCP static analysis tool |
| `README.md` | Add more example queries with expected output |
| `prompts.py` | Improve a system prompt to produce better structured output |
| `evaluator.py` | Improve the score parsing regex for edge cases |
| `docs/` | Add a mapping to CrewAI or AutoGen concepts (like the LangGraph mapping) |

---

## 🐛 Reporting Bugs

Open a GitHub Issue with:
1. The exact error message and stack trace
2. Which Python version you are using (`python --version`)
3. Which LLM provider and model you are using
4. The exact steps to reproduce the issue

---

## 💬 Questions

If you are learning and have a question about *why* something works the way it does, open a **Discussion** (not an Issue). This helps other learners too.

---

Thank you for helping make AI education more accessible! 🎓
