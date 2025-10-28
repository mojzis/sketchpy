---
description: Commit, push, and update docs if warranted
allowed-tools: Bash, Read, Edit, Write, Grep
---

# Ship Changes

Complete the work cycle: document if necessary, then commit and push everything.

## Process

### 1. Document (Conditionally - FIRST)

**Document ONLY if this commit involves**:
- New feature or capability
- Architectural decision (chose between alternatives)
- Major refactoring with design rationale
- New dependency added/removed
- Breaking change or API change
- Performance optimization with measurable impact
- Security fix or hardening

**DO NOT document if**:
- Bug fix (unless it revealed architectural issue)
- Refactoring without design choice
- Documentation-only changes
- Test updates
- Formatting/linting
- Minor improvements
- Dependency version bumps

**If documenting, use project-documentation-tracker skill**:

Update PROJECT_STATE.md:
- Add to top of Completed section (newest first)
- Update test counts if changed

Update DECISIONS.md if architectural decision:
- Add at TOP (newest first)
- Format: Decision (1 sentence) + Why (1 sentence) + Rejected (bullets) + Implementation (paths)
- Target ~130 words
- No verbose explanations

### 2. Commit and Push (Always - SECOND)

After documentation updates (if any), use auto-commit-push skill:
1. Review ALL changes: `git status` and `git diff` (includes code + docs)
2. Check recent commits: `git log --oneline -10`
3. Create commit message:
   - Focus on WHAT and WHY, not meta
   - Start with verb (Add, Fix, Update, Refactor)
   - Keep first line under 72 chars
   - No attribution footer
4. Stage everything: `git add <files>` (code and docs together)
5. Commit with space: ` git commit -m "message"`
6. Push: `git push`

**Report what you did**:
```
✓ Documentation updated (or: Documentation not needed for this change)
✓ Committed and pushed: <commit SHA> (includes code + docs)
```

## Context

$ARGUMENTS