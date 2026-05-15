# Skills


# Agents



# Agent Development Workflow

## Model Definitions
In this workflow, the following models are mapped to specific functional roles:
* **Strategy-Model**: Gemini 3.1 Pro (Optimized for broad reasoning and long-context logic)
* **Technical-Model**: GPT 5.5 (Optimized for agentic execution, code, and security)
* **Critic-Model**: Opus 4.7 (Optimized for factual accuracy and meticulous auditing)

---

## Phase 1: Conceptualization
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Brainstorm** | **Strategy-Model** | Generate high-level concepts and explore the "What" and "Why." |
| **Inquisit** | **Critic-Model** | Review the concept; poke holes in logic and identify early risks. |

---

## Phase 2: Architecture & Planning
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Architect** | **Strategy-Model** | Generate the perfect technical implementation logic and system design. |
| **Inquisit** | **Critic-Model** | Review the technical implementation for edge cases and dependency conflicts. |
| **Plan** | **Technical-Model** | Plan the implementation steps into a tactical, actionable backlog. |
| **Inquisit** | **Critic-Model** | Review the plan for feasibility, timelines, and resource constraints. |

---

## Phase 3: Implementation Loop
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Setup** | **Technical-Model** | Setup the project environment, folder structure, and boilerplate code. |
| **Plan (Iterative)** | **Technical-Model** | Plan the next specific adjustment based on the current build state. |
| **Build** | **Technical-Model** | Implement the adjustment, run code, and fix errors autonomously. |

---

## Phase 4: Production Readiness
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Secure** | **Technical-Model** | Perform a security audit and red-teaming before production deployment. |
| **Review** | **Critic-Model** | Conduct a general audit to ensure the final product matches the original intent. |
