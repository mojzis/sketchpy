---
name: project-documentation-tracker
description: Maintain PROJECT_STATE.md and DECISIONS.md files tracking implementation status, architecture decisions, completed work, and trade-offs. Use when completing tasks, making architectural decisions, or finishing implementation work that should be documented for future reference.
allowed-tools: Read, Write, Edit
---

# Project Documentation Tracker

Maintain two living documentation files that capture project evolution, implementation status, and decision rationale. Update these files after completing tasks or making significant decisions.

## When to Use This Skill

Activate this skill when:
- Completing a feature or task
- Making architectural or design decisions
- Finishing a coding session with notable progress
- Resolving technical trade-offs
- Implementing new patterns or approaches
- Identifying constraints or dependencies

## Documentation Files

### 1. PROJECT_STATE.md

Track the current state of the project:
- **Implementation Status**: What's completed vs. in progress
- **Architecture Decisions**: Key structural choices made
- **Code Patterns**: Established patterns being used
- **Known Constraints**: Technical limitations and dependencies
- **Next Steps**: Clear priorities for upcoming work

### 2. DECISIONS.md

Document decision-making process:
- **Decision Made**: Clear statement of what was decided
- **Context**: Why the decision was needed
- **Options Considered**: Alternative approaches evaluated
- **Rationale**: Why this option was chosen
- **Trade-offs**: What was gained and what was sacrificed
- **Rejected Alternatives**: What was considered but not chosen, and why

## Instructions

### After Completing Any Task

1. **Read existing documentation**
   ```bash
   # Check if files exist
   cat PROJECT_STATE.md 2>/dev/null || echo "PROJECT_STATE.md not found"
   cat DECISIONS.md 2>/dev/null || echo "DECISIONS.md not found"
   ```

2. **Update PROJECT_STATE.md**
   - Move completed items from "In Progress" to "Completed"
   - Add new architectural patterns or decisions to relevant sections
   - Update known constraints if any were discovered
   - Document new code patterns if established
   - Update "Next Steps" based on current priorities

3. **Update DECISIONS.md (if applicable)**
   - Add entry for any significant decision made
   - Document trade-offs considered
   - Note rejected alternatives with rationale

4. **Keep entries concise but complete**
   - Use bullet points for clarity
   - Include dates for decisions (YYYY-MM-DD format)
   - Link related decisions when applicable
   - Be specific about what changed and why

### File Structure Guidelines

**PROJECT_STATE.md Structure:**
```markdown
# Project State

Last Updated: YYYY-MM-DD

## Overview
[Brief project description and current phase]

## Implementation Status

### Completed
- [Feature/Component] (YYYY-MM-DD)
  - Brief description of what was implemented
  - Key outcomes or changes

### In Progress
- [Feature/Component]
  - Current status and blockers if any
  - Expected completion approach

### Planned
- [Feature/Component]
  - Why it's needed
  - Dependencies

## Architecture Decisions

### [Component/System Name]
- **Decision**: What was decided
- **Rationale**: Why this approach
- **Date**: YYYY-MM-DD

## Code Patterns

### [Pattern Name]
- **Usage**: Where and how it's used
- **Example**: Brief code reference or file location
- **Rationale**: Why this pattern was chosen

## Known Constraints

### Technical
- [Constraint description]
  - Impact on development
  - Workarounds if any

### Dependencies
- [Dependency name/description]
  - Version or requirement details
  - Why it's needed

## Next Steps

1. [Priority 1 task]
   - Why it's next
   - Prerequisites

2. [Priority 2 task]
   - Context
```

**DECISIONS.md Structure:**
```markdown
# Architectural and Implementation Decisions

## Decision Log Format
Each decision includes: Context, Decision, Rationale, Trade-offs, Alternatives Considered

---

## [Decision Title] (YYYY-MM-DD)

**Status**: Accepted | Superseded | Deprecated

**Context**
[What problem or need prompted this decision? What constraints exist?]

**Decision**
[What was decided? Be specific and actionable.]

**Rationale**
[Why was this the best choice? What factors influenced the decision?]

**Trade-offs**
- **Pros**: What this approach provides
- **Cons**: What this approach sacrifices or makes more difficult

**Alternatives Considered**
1. **[Alternative 1]**
   - Description
   - Why rejected: [Specific reason]

2. **[Alternative 2]**
   - Description
   - Why rejected: [Specific reason]

**Related Decisions**
- Links to related decisions if any

---
```

## Examples

### Example 1: After Implementing Authentication

**PROJECT_STATE.md Update:**
```markdown
### Completed
- Authentication System (2025-10-26)
  - Implemented JWT-based authentication
  - Added token refresh mechanism
  - Created middleware for protected routes

## Code Patterns

### JWT Authentication Pattern
- **Usage**: All API routes requiring authentication use `requireAuth` middleware
- **Example**: `src/middleware/auth.js`, applied in `src/routes/api.js`
- **Rationale**: Stateless authentication enables horizontal scaling

## Known Constraints

### Technical
- JWT tokens expire after 15 minutes
  - Impact: Requires refresh token implementation
  - Workaround: Automatic refresh on client side
```

**DECISIONS.md Entry:**
```markdown
## JWT vs Session-Based Authentication (2025-10-26)

**Status**: Accepted

**Context**
Needed to implement user authentication for the API. System needs to scale horizontally across multiple servers without shared state.

**Decision**
Use JWT (JSON Web Tokens) for stateless authentication with short-lived access tokens (15 min) and longer-lived refresh tokens (7 days).

**Rationale**
- Enables stateless authentication (no server-side session storage)
- Supports horizontal scaling without session replication
- Widely supported by client libraries
- Can include custom claims for authorization

**Trade-offs**
- **Pros**: Stateless, scalable, no database lookup per request, self-contained
- **Cons**: Cannot invalidate tokens before expiration, larger payload than session IDs, needs refresh mechanism

**Alternatives Considered**
1. **Session-based authentication with Redis**
   - Why rejected: Adds Redis dependency, requires session replication, creates coupling

2. **OAuth2 with third-party providers only**
   - Why rejected: Requires users to have external accounts, less control over auth flow

**Related Decisions**
- Token expiration strategy (see below)
```

### Example 2: After Choosing Database

**PROJECT_STATE.md Update:**
```markdown
## Architecture Decisions

### Data Storage
- **Decision**: PostgreSQL for primary database with JSON columns for flexible schemas
- **Rationale**: Need relational integrity for core data, but flexibility for user-generated content
- **Date**: 2025-10-26

## Dependencies
- PostgreSQL 15+
  - Required for JSON indexing features
  - Using connection pooling via pg-pool
```

**DECISIONS.md Entry:**
```markdown
## PostgreSQL vs MongoDB for Data Storage (2025-10-26)

**Status**: Accepted

**Context**
Application needs to store structured user data, relationships between entities, and some flexible schema fields for user-generated content.

**Decision**
Use PostgreSQL with JSONB columns for flexible fields rather than MongoDB.

**Rationale**
- Strong ACID guarantees needed for financial data
- Complex relationships between users, organizations, and resources
- JSONB provides flexibility where needed without sacrificing consistency
- Team has more PostgreSQL experience

**Trade-offs**
- **Pros**: ACID compliance, powerful joins, mature ecosystem, flexible with JSONB
- **Cons**: More complex schema migrations, less flexible than pure document store

**Alternatives Considered**
1. **MongoDB**
   - Why rejected: Weaker consistency guarantees, team less familiar, over-engineered for our use case

2. **PostgreSQL + Elasticsearch**
   - Why rejected: Added operational complexity, PostgreSQL full-text search sufficient for current needs

3. **SQLite**
   - Why rejected: Cannot handle expected concurrent write load
```

### Example 3: After Adopting Code Pattern

**PROJECT_STATE.md Update:**
```markdown
## Code Patterns

### Repository Pattern for Data Access
- **Usage**: All database access goes through repository classes in `src/repositories/`
- **Example**: `UserRepository`, `OrganizationRepository` in `src/repositories/`
- **Rationale**: Abstracts database logic from business logic, makes testing easier, enables caching layer

## In Progress
- Migrate legacy direct database calls to repository pattern
  - 60% complete, focusing on user management modules
  - Blocking: Some complex queries need optimization before migration
```

## Best Practices

1. **Update documentation immediately after completing work** - Context is fresh
2. **Be specific with dates** - Helps understand evolution over time
3. **Link decisions to implementation** - Reference specific files or modules
4. **Keep entries scannable** - Use bullet points and clear headers
5. **Document the "why" not just the "what"** - Future you needs context
6. **Update status markers** - Move items through Planned → In Progress → Completed
7. **Note blockers explicitly** - Helps identify what needs attention
8. **Cross-reference related decisions** - Decisions often build on each other
9. **Keep PROJECT_STATE.md current** - It should always reflect reality
10. **Don't delete decisions** - Mark as superseded instead, preserving history

## Common Mistakes to Avoid

- ❌ Only documenting decisions, not implementation status
- ❌ Writing vague decisions without specific rationale
- ❌ Forgetting to update status when work is completed
- ❌ Not documenting rejected alternatives
- ❌ Making entries too long and unreadable
- ❌ Skipping documentation for "small" decisions (they accumulate)
- ❌ Not dating entries
- ❌ Documenting implementation details instead of decisions and status

## Workflow Integration

**Typical Flow:**
1. Complete a task or feature
2. Invoke this skill: "Update project documentation for [completed work]"
3. Read existing PROJECT_STATE.md and DECISIONS.md
4. Identify what sections need updates
5. Add/update entries following the templates
6. Commit both files with descriptive commit message

**Commit Message Format:**
```
docs: update project state and decisions

- Mark authentication system as complete
- Document JWT decision and rationale
- Update code patterns with new repository approach
```

## Quick Reference

**When to update PROJECT_STATE.md:**
- ✅ Completed any feature or component
- ✅ Established a new code pattern
- ✅ Discovered a constraint or dependency
- ✅ Changed project architecture
- ✅ Updated priorities

**When to add to DECISIONS.md:**
- ✅ Made technology choice (database, framework, library)
- ✅ Chose between architectural approaches
- ✅ Decided on code patterns or conventions
- ✅ Rejected significant alternatives
- ✅ Made trade-off between competing concerns
- ✅ Changed direction from previous decision

## Initial Setup

If files don't exist, create them with:

**PROJECT_STATE.md:**
```markdown
# Project State

Last Updated: [Current Date]

## Overview
[Brief description of the project]

## Implementation Status

### Completed
- Initial project setup ([Date])

### In Progress
- [Current work]

### Planned
- [Future work]

## Architecture Decisions

[Will be populated as decisions are made]

## Code Patterns

[Will be populated as patterns emerge]

## Known Constraints

### Technical
- [List constraints as discovered]

### Dependencies
- [List dependencies as added]

## Next Steps

1. [Next priority]
```

**DECISIONS.md:**
```markdown
# Architectural and Implementation Decisions

## Decision Log Format
Each decision includes: Context, Decision, Rationale, Trade-offs, Alternatives Considered

---

## Initial Project Structure ([Date])

**Status**: Accepted

**Context**
Starting new project, need to establish basic structure and tooling.

**Decision**
[Document your initial decisions here]

**Rationale**
[Why these choices were made]

**Trade-offs**
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

**Alternatives Considered**
[Other options evaluated]

---
```

## Integration with Development Workflow

This skill works best when:
- Run at the end of each development session
- Invoked after merging PRs or completing milestones
- Used during code reviews to capture decision context
- Applied when onboarding shows documentation gaps
- Executed when pivoting from previous approaches

The goal is to maintain living documentation that:
- Helps new team members understand the project quickly
- Prevents re-litigating past decisions
- Provides clear status for async teams
- Documents the evolution of thinking
- Preserves institutional knowledge