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
- **Avoid meta information**: Don't mention that tests pass, builds succeed, or other process details (these are implicit in the act of committing)
- Focus on WHAT changed and WHY, not process/verification steps

Example:
```
Add grid() method to Canvas for coordinate visualization

Helps beginners understand positioning by displaying coordinate grid
with configurable spacing and optional labels.
```

**Bad examples** (too meta):
- ❌ "All tests passing after fixing bug"
- ❌ "Update code and verify it works"
- ❌ "Changes complete and tested"

**Good examples** (focus on substance):
- ✅ "Fix off-by-one error in grid coordinate labels"
- ✅ "Update grid() to support custom label formatting"
- ✅ "Add optional axis labels to coordinate grid"

## Instructions

When invoked, use the Task tool to launch a general-purpose agent that will handle the complete commit and push workflow:

1. Review changes with `git status` and `git diff`
2. Analyze recent commits to match project style
3. Create a concise, focused commit message that:
   - Describes WHAT changed and WHY
   - Avoids meta information (test status, verification steps)
   - Follows conventional commit format
   - Includes the standard footer with Claude Code attribution
4. Stage all relevant files
5. Create the commit using a command that starts with a space (` git commit`) to avoid cluttering shell history
6. Push to remote (with safety checks)

**Important**: Always prefix the git commit command with a space to prevent it from being saved in shell history. This keeps the command line history clean and focused on interactive commands.

Example:
```bash
git add file.py
 git commit -m "$(cat <<'EOF'
Your commit message here
EOF
)"
git push
```

The agent will autonomously handle all git operations and ensure the commit message follows best practices without meta information.

## Safety Features

- Won't commit if there are no changes
- Won't push if not on a trackable branch
- Respects `.gitignore` patterns
- Shows confirmation of what was committed
