# OpenCode Configuration

Welcome to the OpenCode configuration folder. This directory contains agent definitions, skills, and configuration for managing AI-driven development workflows.

## 📁 Folder Structure

```
opencode/
├── README.md        # This file
├── AGENTS.md        # Detailed agent specifications
├── opencode.jsonc   # Primary OpenCode configuration
├── tui.jsonc        # Terminal UI configuration
├── agents/          # Agent definitions
└── skills/          # Specialized capability modules
```

## 🤖 Agents

This workflow defines six specialized agents that work together in distinct phases:

| Agen           | Phase                | Purpose                                                |
| :---           | :---                 | :---                                                   |
| **brainstorm** | Conceptualization    | Generate high-level concepts and explore possibilities |
| **inquisit**   | Review & Validation  | Challenge assumptions and identify risks/edge cases    |
| **setup**      | Implementation       | Prepare project environment and boilerplate            |
| **test**       | Implementation       | Create and run test suites                             |
| **secure**     | Production Readiness | Security audit and red-teaming                         |
| **review**     | Production Readiness | Final audit for specification alignment                |

## 🛠️ Skills

Skills are modular packages that extend agent capabilities with specialized knowledge and workflows:

- **create-design-md** - Generate structured design documents with best practices
- **find-skills** - Discover and install skills from the ecosystem
- **frontend-design** - Frontend design patterns and component guidance
- **handoff** - Manage project handoffs and documentation
- **shadcn-svelte** - Integration patterns for Shadcn/Svelte components
- **svelte-code-writer** - Code generation for Svelte projects
- **svelte-core-bestpractices** - Svelte development best practices

## 🔄 Development Workflow

The agent workflow follows a structured four-phase approach:

### Model Definitions
Three specialized models handle different functional roles:
* **Strategy-Model**: Broad reasoning and long-context logic
* **Technical-Model**: Agentic execution, code, and security
* **Critic-Model**: Factual accuracy and meticulous auditing

#### Recommended Models (May 2026)
These models are the preferred choices for each role as of May 2026. You can also use the same model for every role.
* **Strategy-Model**: Gemini 3.1 Pro
  * Open-weight alternative: **MiMo-V2.5-Pro**
* **Technical-Model**: GPT 5.5
  * Open-weight alternative: **DeepSeek V4Pro (Max)**
* **Critic-Model**: Opus 4.7
  * Open-weight alternative: **Kimi K2.6**

---

### Phase 1: Conceptualization
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Brainstorm** | **Strategy-Model** | Generate high-level concepts and explore the "What" and "Why." |
| **Inquisit** | **Critic-Model** | Review the concept; poke holes in logic and identify early risks. |

---

### Phase 2: Architecture & Planning
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Architect** | **Strategy-Model** | Generate the perfect technical implementation logic and system design. |
| **Inquisit** | **Critic-Model** | Review the technical implementation for edge cases and dependency conflicts. |
| **Plan** | **Technical-Model** | Plan the implementation steps into a tactical, actionable backlog. |
| **Inquisit** | **Critic-Model** | Review the plan for feasibility, timelines, and resource constraints. |

---

### Phase 3: Implementation Loop
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Setup** | **Technical-Model** | Setup the project environment, folder structure, and boilerplate code. |
| **Plan (Iterative)** | **Technical-Model** | Plan the next specific adjustment based on the current build state. |
| **Build** | **Technical-Model** | Implement the adjustment, run code, and fix errors autonomously. |

---

### Phase 4: Production Readiness
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Secure** | **Technical-Model** | Perform a security audit and red-teaming before production deployment. |
| **Review** | **Critic-Model** | Conduct a general audit to ensure the final product matches the original intent. |
