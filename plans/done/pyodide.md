# Pyodide Upgrade Plan: 0.25.0 → 0.29.0

**Current Version:** Pyodide 0.25.0 (Python 3.11.x)  
**Target Version:** Pyodide 0.29.0 (Python 3.13.2)  
**Project:** sketchpy educational graphics library

---

## Version Progression Summary

### 0.25.0 → 0.26.0 (May 2024)
**Python:** 3.11.x → 3.12.1  
**Breaking Changes:**
- Wheel tag changed to `pyodide_2024_0_wasm32`
- exit() behavior changed (shuts down interpreter in 0.26.0-0.26.1, reverted in 0.27.0+)

### 0.26.0 → 0.27.0 (August 2024)
**Python:** 3.12.1 → 3.12.3  
**Key Changes:**
- Stack switching improvements
- iOS compatibility fixes
- `time.sleep()` now uses stack switching

### 0.27.0 → 0.28.0 (September 2024)
**Python:** 3.12.3 → 3.12.7  
**Key Changes:**
- Shared libraries now loaded locally (breaking)
- Added unix-timezones module
- Performance improvements

### 0.28.0 → 0.29.0 (October 2024)
**Python:** 3.12.7 → 3.13.2  
**Key Changes:**
- Added `checkAPIVersion` option to loadPyodide
- JsProxy deprecations (as_object_map → as_js_json)
- Node.js package caching fixes

---

## Impact Assessment for sketchpy

### ✅ Low Risk Changes
1. **Python 3.11 → 3.13 compatibility**: sketchpy uses basic Python (no stdlib changes affecting us)
2. **Performance improvements**: Stack switching, wasm-gc optimizations (transparent)
3. **Bug fixes**: iOS compatibility, Node.js caching, scipy fixes

### ⚠️ Medium Risk Changes
1. **Wheel tag change** (0.26.0): Shouldn't affect us (we don't build custom packages)
2. **Shared library loading** (0.28.0): Shouldn't affect us (no C extensions)
3. **JsProxy API deprecations** (0.29.0): Check if we use `as_object_map()` anywhere

### 🔴 Breaking Changes to Address
**None directly affecting sketchpy's current usage pattern** - we:
- Don't use custom packages/wheels
- Don't use exit() or SystemExit
- Don't call shared library loading
- Use basic Canvas API (pure Python SVG generation)

---

## Testing Strategy

### Pre-Upgrade Checks

```bash
# 1. Document current behavior
# Run all tests with Pyodide 0.25.0 and save baseline
uv run pytest -v > tests/baseline_0.25.0.txt

# 2. Check for deprecated API usage
grep -r "as_object_map" static/js/
grep -r "extractDir" static/js/
grep -r "exit()" sketchpy/
```

### Upgrade Steps

#### Phase 1: Update CDN URLs (5 min)

**Files to modify:**
1. `static/js/security/config.js`
2. `static/js/pyodide-worker.js` (if it has hardcoded URL)
3. Any templates with CDN references

**Changes:**
```javascript
// OLD (0.25.0)
PYODIDE_VERSION: '0.25.0',
PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',

// NEW (0.29.0)
PYODIDE_VERSION: '0.29.0',
PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.29.0/full/',
```

**Worker changes:**
```javascript
// OLD
importScripts('https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js');
pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
});

// NEW
importScripts('https://cdn.jsdelivr.net/pyodide/v0.29.0/full/pyodide.js');
pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.29.0/full/'
});
```

#### Phase 2: Test Core Functionality (30 min)

**Test matrix:**

| Test | 0.25.0 Baseline | 0.29.0 Result | Status |
|------|----------------|---------------|--------|
| Pyodide loads in worker | ✓ | ? | |
| Basic Canvas creation | ✓ | ? | |
| Shape drawing (rect, circle) | ✓ | ? | |
| SVG output generation | ✓ | ? | |
| Color classes accessible | ✓ | ? | |
| Palette classes accessible | ✓ | ? | |
| Method chaining works | ✓ | ? | |
| Keyboard shortcuts work | ✓ | ? | |
| Lesson starter code runs | ✓ | ? | |
| Error messages clear | ✓ | ? | |

**Test commands:**
```bash
# Browser tests (critical path)
uv run pytest tests/test_browser.py -v

# Lesson tests (ensure all starter code works)
uv run pytest tests/test_lessons.py -v

# Build tests (ensure generation works)
uv run pytest tests/test_build.py -v

# Full suite
uv run pytest -v
```

#### Phase 3: Performance Validation (15 min)

**Benchmark Pyodide load time:**

```javascript
// Add to test or development page
const start = performance.now();
const pyodide = await loadPyodide({
    indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.29.0/full/'
});
const loadTime = performance.now() - start;
console.log(`Pyodide load time: ${loadTime}ms`);

// Expected: Similar or faster than 0.25.0 (stack switching improvements)
```

**Benchmark code execution:**

```python
# Test with nested loops (Lesson 8-9 complexity)
can = Canvas(800, 600)
for row in range(5):
    for col in range(5):
        can.circle(50 + col * 150, 50 + row * 100, 30, fill=Color.RED)
```

**Expected outcome:** Comparable or better performance due to Python 3.13 JIT improvements.

#### Phase 4: Python 3.13 Compatibility (30 min)

**Check for Python 3.13 changes affecting sketchpy:**

1. **Type hints**: Python 3.13 has improved type system
   - Review `sketchpy/shapes.py` for any type hint issues
   - Test: `python -c "import sketchpy.shapes"`

2. **String/unicode changes**: Should not affect us
   - We only use basic string operations

3. **Deprecations removed**: Check if we use any
   - `imp` module (removed)
   - `distutils` (removed)
   - None of these used in sketchpy

**Action:** No changes needed - sketchpy uses stable Python features.

#### Phase 5: Browser Compatibility (15 min)

**Test in multiple browsers:**

| Browser | Version | Pyodide Loads | Code Executes | Notes |
|---------|---------|---------------|---------------|-------|
| Chrome | Latest | ? | ? | |
| Firefox | Latest | ? | ? | |
| Safari | Latest | ? | ? | iOS fix in 0.27.1 |
| Edge | Latest | ? | ? | |

**Manual test steps:**
1. Open `https://localhost:8000/lessons/01-first-flower.html`
2. Verify Pyodide loads (check console)
3. Run starter code (Cmd/Ctrl+Enter)
4. Verify SVG renders
5. Test multiple executions (no memory leaks)

#### Phase 6: Security Layer Compatibility (20 min)

**Verify security implementation still works:**

Since the security plan uses Pyodide 0.25.0 as reference, update and test:

1. **Import blocking still works:**
   ```python
   # Should be blocked
   import js
   import os
   eval("print('blocked')")
   ```

2. **Canvas size limits enforced:**
   ```python
   # Should fail
   can = Canvas(5000, 5000)
   ```

3. **Timeout still terminates:**
   ```python
   # Should timeout after 5 seconds
   while True:
       pass
   ```

4. **AST validation still catches issues:**
   ```python
   # Should be caught before execution
   import __builtins__
   ```

**Update security config:**
```javascript
// static/js/security/config.js
export const SecurityConfig = {
    PYODIDE_VERSION: '0.29.0',  // Updated
    PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.29.0/full/',  // Updated
    // ... rest unchanged
};
```

---

## Rollback Plan

If issues arise:

```javascript
// Revert to 0.25.0 (tested, known working)
PYODIDE_VERSION: '0.25.0',
PYODIDE_CDN: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/',
```

**CDN availability:** jsDelivr keeps all versions available indefinitely.

---

## Implementation Checklist

### Pre-Upgrade
- [ ] Run all tests with 0.25.0 and save baseline results
- [ ] Document current Pyodide load time
- [ ] Check for deprecated API usage in codebase
- [ ] Review Python 3.13 changelog for breaking changes

### Upgrade
- [ ] Update `static/js/security/config.js` (PYODIDE_VERSION, PYODIDE_CDN)
- [ ] Update `static/js/pyodide-worker.js` (importScripts URL, indexURL)
- [ ] Update any template files with hardcoded CDN URLs
- [ ] Update `SECURITY_IMPLEMENTATION_PLAN.md` (reference to 0.29.0)

### Testing
- [ ] Browser tests pass (9 tests)
- [ ] Build tests pass (11 tests)
- [ ] Lesson tests pass (12 tests)
- [ ] Snippet tests pass (5 tests)
- [ ] Server tests pass (2 tests)
- [ ] Manual browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Security validation tests pass
- [ ] Performance benchmarks comparable or better

### Documentation
- [ ] Update PROJECT_STATE.md (Pyodide version)
- [ ] Update DECISIONS.md (upgrade decision)
- [ ] Update CLAUDE.md if version referenced
- [ ] Add entry to DECISIONS.md about upgrade

### Post-Upgrade
- [ ] Monitor for 1 week for any issues
- [ ] Check browser console for new warnings
- [ ] Verify lesson completion rates unchanged
- [ ] Update curriculum docs if Python 3.13 features worth teaching

---

## Python 3.13 New Features (Optional Enhancements)

If we want to leverage Python 3.13 improvements:

### 1. JIT Compiler
Python 3.13 includes a Just-In-Time compiler that can improve performance
- **For us:** Nested loops in Lesson 8-9 might execute faster
- **Action:** Benchmark existing lesson code, no changes needed

### 2. Improved Error Messages
Tracebacks now highlighted in color by default
- **For us:** Better error messages for students
- **Action:** Test error handling in lessons, ensure color rendering works

### 3. Free-Threaded Mode (PEP 703)
Experimental support for running without GIL
- **For us:** Not relevant (single-threaded browser environment)
- **Action:** None

### 4. Type Parameter Defaults
Type parameters now support default values
- **For us:** Could improve Canvas type hints
- **Action:** Optional enhancement in future

---

## Estimated Time

| Phase | Duration |
|-------|----------|
| Pre-upgrade checks | 15 min |
| Update CDN URLs | 5 min |
| Test core functionality | 30 min |
| Performance validation | 15 min |
| Python 3.13 compatibility | 30 min |
| Browser compatibility | 15 min |
| Security layer compatibility | 20 min |
| Documentation updates | 20 min |
| **Total** | **~2.5 hours** |

---

## Risk Assessment

**Overall Risk: LOW** ✅

### Why Low Risk?
1. **No breaking API changes** affecting our usage pattern
2. **Pure Python library** (no C extensions, no custom packages)
3. **Simple use case** (Canvas API, SVG generation)
4. **Easy rollback** (change CDN URL back)
5. **Incremental Python version** (3.11 → 3.13, backward compatible)

### Potential Issues
1. **Load time regression:** Monitor performance benchmarks
2. **Browser quirks:** Test in all browsers (especially Safari/iOS)
3. **Security layer breaks:** Validate import blocking still works
4. **Student code breaks:** Run all lesson tests

### Mitigation
- Keep 0.25.0 as fallback in config (feature flag)
- Test thoroughly before deploying to students
- Monitor error rates post-upgrade

---

## Recommendation

**Proceed with upgrade** - benefits outweigh risks:

### Benefits
1. **Python 3.13** - latest features, JIT compiler
2. **Performance** - stack switching, wasm-gc improvements
3. **Bug fixes** - iOS, Node.js, scipy improvements
4. **Security** - latest Pyodide security updates
5. **Future-proof** - stay current with Pyodide development

### Timeline
1. **Week 1:** Implement and test in development
2. **Week 2:** Deploy to staging, monitor
3. **Week 3:** Deploy to production if no issues

---

## Files to Modify

```
sketchpy/
├── static/
│   └── js/
│       ├── security/
│       │   └── config.js              # Update PYODIDE_VERSION, PYODIDE_CDN
│       └── pyodide-worker.js          # Update importScripts, indexURL
│
├── SECURITY_IMPLEMENTATION_PLAN.md   # Update version references
├── PROJECT_STATE.md                   # Add upgrade entry
├── DECISIONS.md                       # Document upgrade decision
└── CLAUDE.md                          # Update if version mentioned
```

**Total files:** ~5 files  
**Total changes:** ~10 lines

---

## Success Criteria

✅ **Upgrade successful if:**
1. All 49 tests pass (30 core tests minimum)
2. Pyodide loads in <5 seconds
3. Lesson code executes without errors
4. No new browser console warnings
5. Security validation passes
6. Performance equal or better than 0.25.0

---

## Next Steps

1. **Claude Code**: Implement Phase 1 (update CDN URLs)
2. **Run tests**: `uv run pytest -v`
3. **Manual testing**: Open browser, test lessons
4. **Review results**: Compare to baseline
5. **Document**: Update PROJECT_STATE.md

**Command to start:**
```bash
# 1. Update config files (see above)
# 2. Test
uv run pytest -v
# 3. Manual browser test
uv run srv
# Open https://localhost:8000/lessons/01-first-flower.html
```

---

## Questions for Review

1. Should we skip straight to 0.29.0 or test 0.26, 0.27, 0.28 incrementally?
   - **Recommendation:** Jump to 0.29.0 (no breaking changes affecting us)

2. Should we add a feature flag to switch between versions?
   - **Recommendation:** Yes, for easy rollback:
   ```javascript
   const PYODIDE_VERSION = process.env.PYODIDE_VERSION || '0.29.0';
   ```

3. Should we leverage Python 3.13 features in curriculum?
   - **Recommendation:** Later phase - upgrade first, enhance curriculum later

4. Should we update minimum browser requirements?
   - **Recommendation:** No - 0.29.0 supports same browsers as 0.25.0