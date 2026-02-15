# Workflows System

This directory contains **workflow guides** that act as "slash commands" for external agents (human or AI).

## Available Workflows

### 📚 `/librarian` - Query Codebase Knowledge (NEW)
**File**: `librarian.md`
**Purpose**: Quick query to the local Librarian for codebase knowledge. Use `@librarian` or `/librarian` followed by a question.

### 🏗️ `/agent-architect` - Architecture Design

**Purpose**: Define architecture and tech stack for new projects built from scratch. Use BEFORE `/agent-spec` for greenfield projects.

### `/agent-init` - Initialize Agent Sprint
**File**: `agent-init.md`
**Purpose**: Initialize a new Parent Sprint based on external documents and Librarian context.

### `/agent-microsprint` - Breakdown Micro-Sprints
**File**: `agent-microsprint.md`
**Purpose**: Breakdown a Parent Sprint into individual executable micro-sprints.

### `/agent-detail` - Deep Step Detail
**File**: `agent-detail.md`
**Purpose**: Inject extreme implementation details and verification scripts into a micro-sprint.

### `/agent-research` - Research & Discovery
**File**: `agent-research.md`
**Purpose**: Gather and synthesize information from documents before starting a task. Output to `docs/research/`.

### `/agent-spec` - Create Specification
**File**: `agent-spec.md`
**Purpose**: Transform research findings into a structured spec document (`docs/specs/`) ready for sprint creation.

### `/spec-initializer` - Initialize New Spec
**File**: `system/profiles/default/workflows/specification/initialize-spec.md`
**Purpose**: Initialize spec folder, save raw idea, and prepare for requirements gathering.

### `/spec-shaper` - Research & Shape Spec
**File**: `system/profiles/default/workflows/specification/research-spec.md`
**Purpose**: Gather detailed requirements through targeted questions, visual analysis, and reusability checks.

### `/spec-writer` - Write Detailed Spec
**File**: `system/profiles/default/workflows/specification/write-spec.md`
**Purpose**: Create a detailed specification document for development.

### `/spec-verifier` - Verify Spec
**File**: `system/profiles/default/workflows/specification/verify-spec.md`
**Purpose**: Verify the spec and tasks list against architecture and standards.

### `/task-list-creator` - Create Tasks List
**File**: `system/profiles/default/workflows/implementation/create-tasks-list.md`
**Purpose**: Create a detailed and strategic tasks list for development.

### `/implementer` - Implement Features
**File**: `system/profiles/default/workflows/implementation/implement-tasks.md`
**Purpose**: Implement a feature by following a generated tasks list.

### `/implementation-verifier` - Verify Implementation
**File**: `system/profiles/default/workflows/implementation/verification/create-verification-report.md`
**Purpose**: Verify the end-to-end implementation of a spec and generate a report.

### `/product-planner` - Product Planning
**File**: `system/profiles/default/workflows/planning/create-product-roadmap.md`
**Purpose**: Create and update product documentation including mission and roadmap.

### `/handoff` - Session Handoff Protocol
**File**: `handoff.md`
**Purpose**: Ensures smooth transitions between AI agents or work sessions.
**When to use**: End of session, switching agents, or before major breaks.

## How Workflows Work

1. **Mention**: Reference a workflow using its slash command (e.g., "Follow `/spec-initializer`")
2. **Read**: The external agent reads the workflow file to understand the process
3. **Execute**: The agent follows the documented steps

## Creating New Workflows

To add a new workflow:

1. Create a Markdown file: `.agent/workflows/your_workflow.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   description: Brief description of the workflow
   ---
   ```
3. Write clear, actionable steps in the body
4. Update this README to list the new workflow

## Integration with Supervisor

The Supervisor doesn't directly execute workflows. Instead:
- Workflows guide the **External AI** on how to create proper sprint files
- Sprint files are what the Supervisor actually executes
- This separation of concerns keeps the Supervisor deterministic
