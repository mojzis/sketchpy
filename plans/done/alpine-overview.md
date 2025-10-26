# Alpine.js Multi-Lesson Platform - Overview

## Current State

- ✅ CodeMirror 6 with ES modules + importmap
- ✅ Smart Python autocomplete (Canvas methods, Color palettes)
- ✅ Pyodide integration (direct execution)
- ✅ Working single-lesson UI (2-panel layout)
- ✅ Build system (Jinja2 templating)
- ✅ Dev server with file watching

## Target State

- Alpine.js for reactive UI state
- Multi-lesson architecture (YAML-based)
- 3-panel layout (sidebar + editor + output tabs)
- Progress tracking (localStorage)
- Lesson navigation and landing page
- Optional: Pyodide Web Worker

---

## Implementation Phases

| Phase | Status | File | Description | Time |
|-------|--------|------|-------------|------|
| 0 | ⬜ | [alpine-phase-0.md](./alpine-phase-0.md) | Content Structure (Foundation) | 1-2h |
| 1 | ⬜ | [alpine-phase-1.md](./alpine-phase-1.md) | Build + Alpine.js Setup | 2-3h |
| 2 | ⬜ | [alpine-phase-2.md](./alpine-phase-2.md) | Multi-Panel Alpine UI | 3-4h |
| 3 | ⬜ | [alpine-phase-3.md](./alpine-phase-3.md) | Multi-Lesson Support | 2-3h |
| 4 | ⬜ | [alpine-phase-4.md](./alpine-phase-4.md) | Web Worker (Optional) | 2-3h |

**Total Estimated Time**: 10-15 hours

---

## Quick Start

```bash
# Start with Phase 0
cd /home/jonas/git/sketchpy
cat plans/alpine-phase-0.md

# Follow the tasks and verification steps
# When complete, move to Phase 1
```

---

## Progress Tracking

### Phase 0: Content Structure ⬜
- [ ] Create `lessons/` directory structure
- [ ] Create `lessons.yaml` with metadata
- [ ] Extract lesson content to Markdown
- [ ] Add PyYAML and Markdown dependencies
- [ ] Verify old build still works
- [ ] All tests pass

### Phase 1: Build + Alpine ⬜
- [ ] Update `scripts/build.py` with lesson loader
- [ ] Create `templates/lesson.html.jinja`
- [ ] Create `static/js/app.js` (minimal)
- [ ] Generate dual output (old + new)
- [ ] Alpine.js initializes
- [ ] All tests pass

### Phase 2: Multi-Panel UI ⬜
- [ ] Create template components
- [ ] Implement 3-panel layout
- [ ] Add Alpine state management
- [ ] Collapsible panels with transitions
- [ ] Tabbed output panel
- [ ] Responsive design

### Phase 3: Multi-Lesson ⬜
- [ ] Create 2-3 additional lessons
- [ ] Update `lessons.yaml`
- [ ] Dynamic sidebar with lesson list
- [ ] Progress tracking (localStorage)
- [ ] Landing page with lesson overview
- [ ] All lessons functional

### Phase 4: Web Worker ⬜ (Optional)
- [ ] Create `pyodide-worker.js`
- [ ] Update `app.js` for worker communication
- [ ] Non-blocking code execution
- [ ] Performance verification
- [ ] All tests pass

---

## Architecture Evolution

```
Current (Single Lesson):
┌─────────────────────────────────┐
│  Instructions │  Editor         │
│               │  Canvas         │
└─────────────────────────────────┘

After Phase 2 (3-Panel):
┌──────────┬────────────┬──────────┐
│ Sidebar  │  Editor    │ Output   │
│ (hidden) │            │ Tabs:    │
│          │ Instructions│ -Canvas  │
│          │            │ -Output  │
│          │            │ -Help    │
└──────────┴────────────┴──────────┘

After Phase 3 (Multi-Lesson):
┌──────────┬────────────┬──────────┐
│ Lessons: │  Editor    │ Output   │
│ ✓ Flower │            │          │
│   Garden │ Instructions│  Canvas  │
│   Pattern│            │          │
└──────────┴────────────┴──────────┘
```

---

## Key Technologies

- **Alpine.js**: Lightweight reactive UI (10KB)
- **CodeMirror 6**: Modern code editor (already integrated)
- **Pyodide**: Python in browser (already integrated)
- **Jinja2**: Template engine (already integrated)
- **PyYAML**: Lesson configuration
- **Markdown**: Lesson content authoring

---

## Notes

- Each phase builds on the previous one
- Commit after each phase passes verification
- Old system remains functional through Phase 2
- Phase 4 (Web Worker) is optional but recommended
- Manual browser testing is critical at each phase

---

## Rollback Strategy

Each phase includes rollback instructions. In general:

```bash
# Rollback to previous phase
git log --oneline | head -5  # Find last phase commit
git checkout <commit-hash>

# Or revert specific files
git checkout HEAD~1 -- <file>
```

---

## Getting Help

If stuck:
1. Check phase file for detailed tasks
2. Review verification commands
3. Check browser console for errors
4. Run `uv run pytest -v` for automated checks
5. Refer to `plans/alpine.md` for original design

---

## Success Criteria

**Phase 0**: Lesson content extracted, dependencies added
**Phase 1**: Alpine.js working, dual output generated
**Phase 2**: 3-panel UI functional, all panels responsive
**Phase 3**: Multiple lessons navigable, progress tracked
**Phase 4**: Code runs in worker, UI stays responsive

---

**Start here**: [Phase 0 - Content Structure](./alpine-phase-0.md)
