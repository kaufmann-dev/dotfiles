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

## ⚙️ Configuration

### opencode.jsonc
Primary configuration file for OpenCode settings:
- Model selection (deepseek/deepseek-v4-pro, deepseek/deepseek-v4-flash)
- Default agent selection
- MCP (Model Context Protocol) server configurations
- Tool enablement (websearch, codesearch)

### tui.jsonc
Terminal UI configuration for command-line interactions with OpenCode.

## 🔄 Development Workflow

The agent workflow follows a structured four-phase approach:

### Model Definitions
Three specialized models handle different functional roles:
* **Strategy-Model**: Gemini 3.1 Pro — Broad reasoning and long-context logic
* **Technical-Model**: GPT 5.5 — Agentic execution, code, and security
* **Critic-Model**: Opus 4.7 — Factual accuracy and meticulous auditing

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

## 🚀 Quick Start

1. **Review agents** — See [AGENTS.md](./AGENTS.md) for detailed specifications
2. **Explore skills** — Each skill directory contains a `SKILL.md` with its specification
3. **Configure** — Update `opencode.jsonc` to customize models, MCPs, and tools
4. **Use** — Reference agents and skills in your OpenCode workflows

## 📚 Key Design Principles

Based on embedded best practices:

- **Think Before Coding** — Surface assumptions and tradeoffs explicitly
- **Simplicity First** — Minimum code that solves the problem
- **Surgical Changes** — Touch only what's necessary, match existing style
- **Goal-Driven Execution** — Define success criteria and verify completion

---

*Last updated: May 15, 2026*
