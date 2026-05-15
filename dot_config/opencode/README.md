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

### Model Definitions
Three specialized models handle different functional roles. The table below shows their role, recommended May 2026 model, and an open-weight alternative.

| Role | Purpose | Recommended Model (May 2026) | Open-weight Alternative |
| :--- | :--- | :--- | :--- |
| **Strategy-Model** | Broad reasoning and long-context logic | Gemini 3.1 Pro | MiMo-V2.5-Pro |
| **Technical-Model** | Agentic execution, code, and security | GPT 5.5 | DeepSeek V4Pro (Max) |
| **Critic-Model** | Factual accuracy and meticulous auditing | Opus 4.7 | Kimi K2.6 |

The agent workflow follows a structured four-phase approach:

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
| **Architect** | **Technical-Model** | Generate the perfect technical implementation logic and system design. |
| **Inquisit** | **Critic-Model** | Review the technical implementation for edge cases and dependency conflicts. |
| **Plan** | **Technical-Model** | Plan the implementation steps into a tactical, actionable backlog. |
| **Inquisit** | **Critic-Model** | Review the plan for feasibility, timelines, and resource constraints. |

---

### Phase 3: Setup & Validation
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Setup** | **Technical-Model** | One-pass project initialization: environment, structure, boilerplate, dependencies, and components. |
| **Inquisit** | **Critic-Model** | Review the setup for correctness, dependency completeness, and adherence to the architecture. |

---

### Phase 4: Development Loop 🔁
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Plan** | **Technical-Model** | Plan the next specific adjustment based on the current build state. |
| **Build** | **Technical-Model** | Implement the adjustment, run code, and fix errors autonomously. |

---

### Phase 5: Production Readiness
| Task | Lead Model | Purpose |
| :--- | :--- | :--- |
| **Test** | **Test-Agent** | Validate the implementation with automated tests and ensure stability before audit. |
| **Audit** | **Critic-Model** | Perform the final production readiness audit, covering security, correctness, and specification alignment. |
