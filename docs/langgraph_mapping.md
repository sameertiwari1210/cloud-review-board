# LangGraph Mapping — CSRB Agent State Machine
# Phase 10: Documenting how our manual implementation maps to LangGraph

## Overview

This document maps every component of the CSRB agent to its LangGraph equivalent.
The goal is to show that our hand-rolled implementation follows the same conceptual
model that LangGraph formalises, making it straightforward to migrate if desired.

---

## Conceptual Comparison Table

| CSRB Component | LangGraph Equivalent | Notes |
|---|---|---|
| `main.py` — `run_full_pipeline()` | `StateGraph` + `.compile()` + `.invoke()` | Our function IS the graph; LangGraph makes it declarative |
| `memory.py` / `database.py` | `StateGraph(State)` — typed state dict | LangGraph passes state between nodes automatically |
| `agents/architect.py` | Node function `architect_node(state)` | Same logic, just receives/returns state dict instead of raw strings |
| `agents/security.py` | Node function `security_node(state)` | Receives architect output from state |
| `agents/finops.py` | Node function `finops_node(state)` | Receives architect output from state |
| `agents/sre.py` | Node function `sre_node(state)` | Receives architect output from state |
| `agents/judge.py` | Node function `judge_node(state)` | Receives all three reviews from state |
| `tool_router.py` | Tool node or conditional edge | LangGraph supports `ToolNode` with `tools_condition` routing |
| `evaluator.py` — `run_evaluation_loop()` | Conditional edge with a loop | LangGraph uses `add_conditional_edges` to loop back |
| `document_loader.py` — `keyword_search()` | Custom retriever node | Could be a dedicated `rag_node(state)` that enriches state |
| `prompts.py` | Prompt templates per node | Often stored as `PromptTemplate` or inline strings in LangGraph |
| Sequential pipeline order in `main.py` | `graph.add_edge(A, B)` | Each `add_edge` call maps to one step in our pipeline |

---

## State Mapping

In LangGraph, shared state is a typed `TypedDict`. Here is how our pipeline's
intermediate data maps to a LangGraph state schema:

```python
from typing import TypedDict

class CSRBState(TypedDict):
    query: str                  # Original user input
    rag_context: str            # Phase 7 — RAG retrieved chunks
    tool_findings: str          # Phase 4 — static tool analysis
    architecture: str           # Phase 1/8 — Architect + Evaluator output
    evaluator_score: int        # Phase 8 — quality score
    evaluator_feedback: str     # Phase 8 — improvement feedback
    security_review: str        # Phase 5 — Security Agent output
    finops_review: str          # Phase 5 — FinOps Agent output
    sre_review: str             # Phase 5 — SRE Agent output
    verdict: str                # Phase 5 — Judge Agent final output
    conversation_id: int        # Phase 6 — SQLite conversation ID
```

---

## Node Mapping

Each agent function in our codebase would become a LangGraph node:

```python
from langgraph.graph import StateGraph

graph = StateGraph(CSRBState)

graph.add_node("rag",       rag_node)        # keyword_search()
graph.add_node("tools",     tool_node)       # route_tools()
graph.add_node("architect", architect_node)  # run_architect_agent()
graph.add_node("evaluator", evaluator_node)  # evaluate_architecture()
graph.add_node("security",  security_node)   # run_security_agent()
graph.add_node("finops",    finops_node)     # run_finops_agent()
graph.add_node("sre",       sre_node)        # run_sre_agent()
graph.add_node("judge",     judge_node)      # run_judge_agent()
```

---

## Edge Routing Mapping

### Sequential edges (our `run_full_pipeline` sequential calls)

```python
graph.add_edge("rag",       "tools")
graph.add_edge("tools",     "architect")
graph.add_edge("architect", "evaluator")
graph.add_edge("security",  "finops")
graph.add_edge("finops",    "sre")
graph.add_edge("sre",       "judge")
graph.set_finish_point("judge")
```

### Conditional edge (our `run_evaluation_loop`)

In our code we loop manually with a `while` loop and a retry counter.
LangGraph expresses this as a conditional edge:

```python
def should_retry(state: CSRBState) -> str:
    if state["evaluator_score"] >= 7:
        return "security"      # pass → move to security review
    if state.get("retry_count", 0) >= 2:
        return "security"      # max retries → accept and move on
    return "architect"         # fail → regenerate

graph.add_conditional_edges(
    "evaluator",
    should_retry,
    {"security": "security", "architect": "architect"}
)
```

### Tool conditional edge (our `route_tools`)

```python
from langgraph.prebuilt import tools_condition

graph.add_conditional_edges(
    "tools",
    tools_condition,           # checks if tools were triggered
    {"tools": "tool_node", "__end__": "architect"}
)
```

---

## Memory / Persistence Mapping

| CSRB Implementation | LangGraph Equivalent |
|---|---|
| `data/memory.json` (Phase 2) | `MemorySaver` checkpointer |
| `database.py` — SQLite (Phase 6) | `SqliteSaver` from `langgraph.checkpoint.sqlite` |
| `load_history()` | `graph.get_state_history(config)` |
| `save_agent_output()` | Automatic — LangGraph saves state at each node |

---

## Key Insight

Our CSRB implementation is a **manual state machine**:
- State is passed as function arguments between agents.
- Edges are function calls in a fixed order in `run_full_pipeline()`.
- Conditional edges are `if/while` statements in `run_evaluation_loop()`.
- Persistence is `save_agent_output()` and `update_memory()` calls.

LangGraph **formalises** the same pattern:
- State is a typed dict passed automatically between nodes.
- Edges are declared with `add_edge` / `add_conditional_edges`.
- Persistence is handled by a checkpointer injected at compile time.

Migrating CSRB to LangGraph would require:
1. Wrapping each agent function to accept and return `CSRBState`.
2. Declaring edges explicitly in the graph builder.
3. Replacing manual SQLite calls with `SqliteSaver`.
4. Replacing the `while` retry loop in `evaluator.py` with a conditional edge.

---

## Summary

> Building from scratch first gave us full visibility into what an agent framework
> actually does under the hood. LangGraph is not magic — it is a clean API over the
> same pattern we implemented manually: nodes, state, edges, and persistence.
