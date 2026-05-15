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

This workflow defines specialized agents that work in pairs — each creative/planning agent has a dedicated reviewer that operates strictly within the same domain.

| Agent               | Phase                | Purpose                                                              |
| :---                | :---                 | :---                                                                 |
| **brainstorm**      | Conceptualization    | Refine rough ideas into a validated `CONCEPT.md`                     |
| **brainstorm_review** | Conceptualization  | Review and strengthen `CONCEPT.md` at the concept level only         |
| **architect**       | Architecture         | Produce `ARCHITECTURE.md` from the validated concept                 |
| **architect_review** | Architecture        | Review and strengthen `ARCHITECTURE.md` at the design level only     |
| **plan**            | Planning             | Produce `PLAN.md` from concept, architecture, and design documents   |
| **plan_review**     | Planning             | Review and strengthen `PLAN.md` for feasibility and completeness     |
| **build**           | Implementation       | Implement the project following the validated plan and documents      |
| **test**            | Validation           | Create and run test suites                                           |
| **audit**           | Production Readiness | Final audit for security, correctness, and specification alignment   |

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

### Document Flow

Each phase produces and validates a specific document that feeds into the next phase:

```
CONCEPT.md ──→ ARCHITECTURE.md ──→ PLAN.md ──→ Implementation
     ↑               ↑                 ↑
  reviewed         reviewed          reviewed
```

---

### Phase 1: Conceptualization
| Step | Agent | Lead Model | Purpose |
| :--- | :--- | :--- | :--- |
| 1a | **brainstorm** | **Strategy-Model** | Explore the idea and produce `CONCEPT.md` |
| 1b | **brainstorm_review** | **Critic-Model** | Review `CONCEPT.md` — concept-level critique only (no technical questions) |

---

### Phase 2: Architecture
| Step | Agent | Lead Model | Purpose |
| :--- | :--- | :--- | :--- |
| 2a | **architect** | **Technical-Model** | Read `CONCEPT.md`, produce `ARCHITECTURE.md` |
| 2b | **architect_review** | **Critic-Model** | Review `ARCHITECTURE.md` — technical design critique only |

---

### Phase 3: Planning
| Step | Agent | Lead Model | Purpose |
| :--- | :--- | :--- | :--- |
| 3a | **plan** | **Technical-Model** | Read `CONCEPT.md` + `ARCHITECTURE.md` + `DESIGN.md`, produce `PLAN.md` |
| 3b | **plan_review** | **Critic-Model** | Review `PLAN.md` — feasibility and completeness critique only |

---

### Phase 4: Implementation
| Step | Agent | Lead Model | Purpose |
| :--- | :--- | :--- | :--- |
| 4 | **build** | **Technical-Model** | Implement from `PLAN.md` + all documents. Works for new and existing projects. |

---

### Phase 5: Validation & Production Readiness
| Step | Agent | Lead Model | Purpose |
| :--- | :--- | :--- | :--- |
| 5a | **test** | **Technical-Model** | Validate the implementation with automated tests |
| 5b | **audit** | **Critic-Model** | Final production readiness audit: security, correctness, spec alignment |
