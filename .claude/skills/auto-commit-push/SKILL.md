---
name: auto-commit-push
description: Automatically create concise commits and push to remote after completing meaningful chunks of work. Use this when a logical unit of work is complete (feature implemented, bug fixed, refactoring done, tests passing).
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Auto-Commit and Push

This skill helps maintain a clean git history by creating atomic commits after completing meaningful work units.

## When to Use

Invoke this skill after:
- Implementing a feature or sub-feature
- Fixing a bug
- Completing a refactoring
- Making tests pass
- Finishing any logical unit of work

**Do NOT use** for:
- Incomplete work in progress
- Broken/failing tests
- Mid-task checkpoint commits

## Process

1. **Review changes**: Check `git status` and `git diff` to understand what changed
2. **Analyze context**: Read recent commits to match the project's commit message style
3. **Create concise message**: Write a 1-2 line commit message focusing on "what" and "why"
4. **Stage and commit**: Add relevant files and create the commit
5. **Push**: Push to the remote repository

## Commit Message Format

Follow the project's existing style (check recent commits). General guidelines:
- Start with a verb (Add, Fix, Update, Refactor, Remove)
- Be specific but concise
- Focus on the change's purpose, not implementation details
- Keep first line under 72 characters

Example:
```
Add grid() method to Canvas for coordinate visualization

Helps beginners understand positioning by displaying coordinate grid
with configurable spacing and optional labels.
```

## Instructions

When invoked, run the git automation script that handles the full workflow:

```bash
bash .claude/skills/auto-commit-push/scripts/commit_and_push.sh
```

The script will:
1. Check for uncommitted changes
2. Display current status and diff
3. Analyze recent commits for style patterns
4. Generate an appropriate commit message
5. Stage relevant files
6. Create the commit
7. Push to remote (with safety checks)

## Safety Features

- Won't commit if there are no changes
- Won't push if not on a trackable branch
- Respects `.gitignore` patterns
- Shows confirmation of what was committed
