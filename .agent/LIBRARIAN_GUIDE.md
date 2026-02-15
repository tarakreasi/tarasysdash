# 📖 Antigravity Librarian Guide

**For: External AI (Antigravity)**

This guide explains how to use the **Local Librarian** - a semantic search engine that remembers the entire project codebase. Use it to stay grounded and avoid hallucinations.

---

## 🧠 Your Role vs Librarian's Role

| You (Antigravity) | Librarian |
|-------------------|-----------|
| Reasoning, planning, coding | Retrieval, memory, facts |
| Think and decide | Store and search |
| May forget context | Never forgets |
| Might hallucinate | Always factual |

**Rule**: When unsure about existing code, **ASK THE LIBRARIAN FIRST**.

---

## 🛠️ How to Use

### Query the Librarian
When you need to find something in the codebase:

```bash
uv run python .agent/workflows/automation/scripts/ask_librarian.py "Your question"
```

**Example Queries**:
- `"How is the embedding service implemented?"`
- `"Where is the deploy script?"`
- `"Show me the database schema"`
- `"Find all workflow definitions"`
- `"What is the alert system spec?"`

### Update the Index
After making significant changes, update the Librarian's knowledge:

```bash
uv run python .agent/workflows/automation/scripts/index_codebase.py
```

---

## 📋 What Gets Indexed

The Librarian indexes **project-relevant files only**:

### ✅ Included
| Directory | Contents |
|-----------|----------|
| `src/`, `internal/`, `cmd/` | Source code |
| `web/src/` | Frontend code |
| `docs/` | Documentation, specs, research |
| `.agent/*.md` | Agent documentation |
| `.agent/workflows/*.md` | Workflow definitions |
| `taraSysDash/` | Project code (if present) |

### ❌ Excluded
| Directory | Reason |
|-----------|--------|
| `.venv/` | Python packages (not project code) |
| `node_modules/` | Node packages |
| `__pycache__/` | Compiled Python |
| `.git/` | Version control |
| `memory/` | Librarian's own database |
| `future/`, `artifak/` | Archived files |

### 📄 File Types Indexed
`.py`, `.md`, `.txt`, `.go`, `.vue`, `.ts`, `.js`, `.json`, `.yaml`, `.yml`, `.sql`

### 📏 Size Limit
Files larger than **100 KB** are skipped.

---

## 🔍 Best Practices

### 1. Query Before Assuming
```
❌ Wrong: "I'll create a new deploy script"
✅ Right: "Let me ask Librarian if deploy script exists"
```

### 2. Be Specific
```
❌ Vague: "How does it work?"
✅ Specific: "How does the EmbeddingService generate vectors?"
```

### 3. Re-index After Major Changes
If you've created many new files, re-index so future queries find them.

### 4. Trust the Librarian
If Librarian says a file exists at path X, it exists. Don't guess alternative paths.

---

## 🏗️ Architecture

```
.agent/workflows/automation/
├── src/librarian/
│   ├── embeddings.py    # Sentence-Transformers (no Ollama!)
│   ├── indexer.py       # Smart whitelist-based indexing
│   ├── retriever.py     # Semantic search
│   └── db_manager.py    # SQLite + sqlite-vec
├── memory/
│   └── librarian.db     # The knowledge base
└── scripts/
    ├── ask_librarian.py     # Query interface
    └── index_codebase.py    # Indexing script
```

### Embedding Model
- **Model**: `all-MiniLM-L6-v2` (Sentence-Transformers)
- **Dimension**: 384
- **No Ollama Required**: Runs purely on Python/PyTorch

---

## 🎯 When to Use Librarian

| Situation | Action |
|-----------|--------|
| Starting a new session | Query: "Summarize current sprint status" |
| Before creating new file | Query: "Does [filename] exist?" |
| Implementing feature | Query: "Existing patterns for [feature]" |
| Debugging | Query: "Where is [function] defined?" |
| Writing spec | Query: "Related specs or research docs" |

---

## 🔗 Integration with Workflows

### `/agent-research`
Uses Librarian to gather existing context before research.

### `/agent-spec`
Queries Librarian for reusable code before writing spec.

### `/agent-init`
Checks Librarian for conflicting implementations.

---

*The Librarian is your memory. Use it wisely.*
