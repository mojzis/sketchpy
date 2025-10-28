---
name: auto-commit-push
description: Create atomic commits and push after completing discrete work units (feature, bugfix, refactoring). Use when tests pass and work is complete.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Auto-Commit and Push

## When to Use

**Trigger after**:
- Feature or sub-feature complete
- Bug fixed
- Refactoring finished
- Tests passing (implied - don't mention in commit message)
- Any discrete, complete work unit

**Skip when**:
- Work in progress
- Tests failing
- Mid-task checkpoint

## Process

1. Check changes: `git status` and `git diff`
2. Review recent commits: `git log --oneline -10` to match project style
3. Write commit message (see format below)
4. Stage files: `git add <files>`
5. Commit: ` git commit -m "message"` (note leading space - keeps shell history clean)
6. Push: `git push`

## Commit Message Format

Match project's existing style. If no clear pattern, use:

```
Verb + what changed (under 72 chars)

Optional: Why this change was needed or what problem it solves.
Wrap at 72 chars.
```

**Focus on WHAT and WHY, not process**:
- ✅ "Fix off-by-one error in grid coordinate labels"
- ✅ "Add optional axis labels to coordinate grid"
- ❌ "All tests passing after fixing bug" (meta information)
- ❌ "Update code and verify it works" (process, not substance)

**Start with verb**: Add, Fix, Update, Refactor, Remove, Implement

**Docs-only commits**: Use "docs: update project state" or similar

**Code + docs commits**: Focus message on code change, don't mention docs

## Example Commands

```bash
# Review changes
git status
git diff

# Check recent style
git log --oneline -10

# Stage and commit
git add src/file.py tests/test_file.py
 git commit -m "Add grid() method to Canvas for coordinate visualization"

# Push (check branch first)
git branch
git push
```

**Important**: Prefix `git commit` with a space (` git commit`) to prevent saving in shell history. This keeps history clean for the user's workflow.

Multi-line commits:
```bash
 git commit -m "$(cat <<'EOF'
First line summary

Optional longer explanation of why this change
was needed and what problem it solves.
EOF
)"
```

## Edge Cases

**No changes**: Check `git status` - if clean, report "no changes to commit"

**Detached HEAD**: Report issue, don't push

**Unpushed commits exist**: Safe to push (will push all)

**Multiple files**: Stage all related to this work unit, may skip unrelated files

**Merge conflicts**: Report - requires manual resolution