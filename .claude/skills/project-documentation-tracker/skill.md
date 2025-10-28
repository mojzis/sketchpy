---
name: project-documentation-tracker
description: Updates PROJECT_STATE.md and DECISIONS.md after completing work or making architectural decisions. Enforces concise format optimized for LLM consumption (70-85% shorter than typical decision logs).
---

# Project Documentation Tracker

## When to Use

**Auto-trigger after**:
- Completing features, phases, or milestones
- Making architectural decisions (choosing between alternatives)
- Significant refactoring with design rationale
- Adding/removing major dependencies

**Manual trigger**:
- User says: "update docs", "document this decision", "update project state"

**Skip when**:
- Minor changes (typos, formatting, small fixes)
- Work still in progress (not yet complete)
- Documentation already current

## Update PROJECT_STATE.md

### Add Completed Features

Add to top of Completed section (newest first):

```markdown
### Completed
- **New Feature** (YYYY-MM-DD) - One sentence description
- **Previous Feature** (YYYY-MM-DD) - One sentence description
```

**Note**: PROJECT_STATE.md tracks what's done and current system state. Track "In Progress" and "Planned" work in Issues, TODO.md, or project boards - not here.

### Update Test Coverage (if changed)

```markdown
### Test Coverage
- Total: X tests (breakdown: unit X, integration Y, browser Z)
```

### Add Constraints (if introducing limitations)

```markdown
### Known Constraints
- **Limitation Name**: Brief description, impact, workaround
```

**Keep brief** - PROJECT_STATE tracks status, not rationale (that goes in DECISIONS.md).

## Update DECISIONS.md

### Format Template

Target: ~130 words per decision (vs 800+ typical)

**Important**: Add new decisions at the TOP of the file (newest first). Recent decisions are most relevant.

```markdown
## Decision Title (YYYY-MM-DD)

**Decision**: One sentence stating what was decided

**Why**: One sentence explaining the core reason

**Rejected**:
- Alternative 1 (reason in parentheses)
- Alternative 2 (reason in parentheses)  
- Alternative 3 (reason in parentheses)
- Alternative 4 (reason in parentheses)

**Implementation**: File paths only
- path/to/changed/file.py
- path/to/other/file.js
```

### What to Cut

Remove these to achieve 70-85% compression:
- Repeated information (e.g., saying "responsive" 4 times)
- Obvious statements ("improves UX", "follows best practices")
- Future possibilities not yet implemented
- Detailed code examples (paths are enough)
- Verbose explanations of well-known concepts
- Self-evident context (Claude already knows what Web Workers are)
- Sales pitch language ("great", "excellent", "smooth")

### What to Keep

Essential information only:
- Core decision (what changed)
- Primary motivation (why it was needed)
- Alternatives considered (brief, with reason)
- Implementation locations (where to find the code)
- Date

### Example Entry

Before (847 words):
"After implementing the Alpine.js-based UI with Pyodide running directly in the main thread, user testing revealed that running Python code would freeze the UI during execution. Users couldn't toggle panels, click buttons, or interact with the interface while code was running. For educational purposes, this is problematic - students may want to check instructions or adjust the canvas size while long-running code executes. Additionally, complex drawings with many shapes could take several seconds, creating a poor user experience..."

After (128 words):
```markdown
## Pyodide Web Worker (2025-10-26)

**Decision**: Move Python execution from main thread to Web Worker (background thread)

**Why**: UI froze during code execution; users couldn't interact while code ran; educational tool needs responsive interface

**Rejected**:
- setTimeout chunking (can't interrupt Pyodide's synchronous execution)
- requestAnimationFrame (same synchronous execution issue)
- Cancel button with page reload (loses user's code and state)
- Modal "Please wait" overlay (doesn't prevent the freezing)
- Warning users about long code (defeats learning purpose)
- SharedArrayBuffer for shared memory (unnecessary complexity)

**Implementation**: 
- static/js/pyodide-worker.js - loads Pyodide, executes via postMessage
- static/js/app.js - worker communication, async result handling
- Tests updated for worker architecture
```

## Validation Before Completing

Check that:
- [ ] Decision title is clear and includes date
- [ ] Decision and Why are each one sentence
- [ ] Rejected alternatives are bullets (3-6 items typical)
- [ ] Each rejected alternative has reason in parentheses
- [ ] Implementation paths listed (if files changed)
- [ ] Entry is under 200 words
- [ ] No redundant or obvious information
- [ ] No sales pitch language
- [ ] PROJECT_STATE.md updated if status changed

## Output Format

After updating documentation, report back concisely:

```
Updated documentation:
- PROJECT_STATE.md: Added [feature] to Completed
- DECISIONS.md: Added decision "[title]" at top (142 words)
```

No need for verbose confirmation - user can review the changes in the files.