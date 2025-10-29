# Math Module - Global Import Implementation

## Summary

Added `math` module as a globally available module in the Pyodide environment, so students don't need to import it.

## Why This Works

**Size**: The `math` module is tiny (~50KB) and is a built-in CPython module, already included in Pyodide by default.

**Performance**: Pre-importing it once at initialization has zero performance impact on lesson execution.

**Safety**: The `math` module is completely safe - it only contains mathematical functions (sin, cos, pi, sqrt, etc.) with no I/O or system access.

## Implementation

### 1. Pyodide Worker (static/js/pyodide-worker.dev.js)

**Lines 60-97**: Pre-import math during initialization
```javascript
await pyodide.runPythonAsync(`
import builtins
import ast
import collections
import sys
import math  // ← Added here

# ... security setup ...

# Allow math in imports
_allowed_modules = {
    'collections', 'collections.abc', '_collections_abc',
    'ast', 'sys', 'builtins', 'typing', 're', 'math'  // ← Added here
}
`)
```

### 2. Error Messages Updated

**Lines 83-89**: Helpful error message
```python
raise ImportError(
    f"Import '{name}' is not allowed.\\n\\n"
    f"You have everything you need:\\n"
    f"  • Canvas, Color (for drawing)\\n"
    f"  • CreativeGardenPalette, CalmOasisPalette, MathDoodlingPalette (color palettes)\\n"
    f"  • math (for trigonometry: math.pi, math.cos(), math.sin())\\n\\n"  // ← Added
    f"No imports needed for the lessons!"
)
```

**Lines 148-158**: AST validation errors
```python
'error': 'Imports are not allowed. You have Canvas, Color, palettes (...), and math already loaded!'
```

### 3. Test Namespace (tests/test_lessons.py)

**Lines 30-41**: Added to test environment
```python
import math
from sketchpy.shapes import MathDoodlingPalette

namespace = {
    'Canvas': Canvas,
    'Color': Color,
    'CreativeGardenPalette': CreativeGardenPalette,
    'CalmOasisPalette': CalmOasisPalette,
    'MathDoodlingPalette': MathDoodlingPalette,
    'math': math,  # ← Added here
    '__builtins__': __builtins__,
}
```

## What's Available

Students can now use `math` directly without importing:

```python
# These all work without "import math"
math.pi        # 3.14159...
math.cos(angle)
math.sin(angle)
math.sqrt(x)
math.floor(x)
math.ceil(x)
# ... and all other math functions
```

## Lessons Using Math

**Theme 3 (Math Doodling):**
- 05-first-mandala (trigonometry for circular arrangement)
- 07-color-lists (same)
- 08-grid-of-mandalas (same)
- 09-growing-spiral (spiral calculations)
- 10-conditional-symmetry (same)
- 11-pattern-functions (same)
- 12-customizable-mandala (same)
- 13-calculated-layouts (same)
- 14-data-driven-art (same)
- 15-meditative-masterpiece (same)

**Theme 1 (Creative Garden):**
- Future lessons using rotation or circular patterns can use it

## Benefits

1. **Simpler for students**: No confusing "you need to import math" error
2. **Consistent with other globals**: Like Canvas, Color, palettes
3. **Zero cost**: Already loaded in Pyodide, no size/performance penalty
4. **Educational**: Students focus on using math, not importing it
5. **Safe**: Math module has no dangerous functions

## Testing

- ✓ All 215 tests pass
- ✓ Lessons using math execute correctly
- ✓ Browser environment has math available
- ✓ Test environment mirrors browser environment

## Size Impact

**Before**: Pyodide bundle ~6.4MB (math already included)
**After**: Pyodide bundle ~6.4MB (no change, just pre-imported)

**Conclusion**: Zero size impact - math is already in Pyodide, we just make it globally available.
