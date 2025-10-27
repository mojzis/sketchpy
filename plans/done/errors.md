# Error Handling Implementation Plan
## Python Drawing Curriculum - Friendly Error Messages

---

## Overview

This plan implements beginner-friendly error messages for the Python drawing curriculum. When students write code that causes errors, they'll see clear explanations, helpful hints, and visual indicators instead of technical Python tracebacks.

**Goal:** Transform frustrating error experiences into learning opportunities that guide students toward solutions.

**Integration:** This error handling system integrates with the security implementation (SECURITY_IMPLEMENTATION_PLAN.md) to provide friendly messages for both code errors and security violations.

---

## Error Flow Through Security Layers

```
User writes code
       ↓
┌─────────────────────────────────────┐
│ Layer 1: Pre-Validation             │
│ (validator.js)                      │
│                                     │
│ Checks:                             │
│ • Forbidden imports                 │
│ • Large canvas size                 │
│ • Suspicious patterns               │
└─────────────────────────────────────┘
       ↓ PASS                    ↓ FAIL
       ↓                         ↓
       ↓                    Format validation error
       ↓                    Show friendly message
       ↓                    (e.g., "Only Canvas and 
       ↓                     Color can be imported")
       ↓
┌─────────────────────────────────────┐
│ Layer 2: Execution with Timeout     │
│ (executor.js + worker)              │
│                                     │
│ Runs code with 5-second limit       │
└─────────────────────────────────────┘
       ↓ TIMEOUT                ↓ SUCCESS/ERROR
       ↓                        ↓
  Format timeout error          ↓
  (e.g., "Code taking too       ↓
   long - try fewer loops")     ↓
                                ↓
                         ┌─────────────────────────────────────┐
                         │ Layer 3: Python Execution           │
                         │ (pyodide-worker.js)                 │
                         │                                     │
                         │ Checks:                             │
                         │ • AST validation                    │
                         │ • Import restrictions               │
                         │ • Canvas size (shapes.py)           │
                         │ • Shape count (shapes.py)           │
                         └─────────────────────────────────────┘
                                ↓ ERROR          ↓ SUCCESS
                                ↓                ↓
                         ┌─────────────────┐    Return SVG
                         │ Layer 4: Error  │    Display result
                         │ Handler         │
                         │                 │
                         │ Formats error   │
                         │ Shows hints     │
                         │ Explains issue  │
                         └─────────────────┘
                                ↓
                         Display friendly error
                         with code context
```



## Security Integration Architecture

The error handling system integrates with the multi-layer security architecture:

```
┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Client-Side Pre-Validation (validator.js)         │
│ - Catches: Forbidden imports, large canvas, dangerous code  │
│ - Action: Show friendly error BEFORE execution              │
└──────────────────────┬──────────────────────────────────────┘
                       │ Pass
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Web Worker Isolation (executor.js)                 │
│ - Catches: Timeouts, worker crashes                         │
│ - Action: Show timeout message, recreate worker             │
└──────────────────────┬──────────────────────────────────────┘
                       │ Executing
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: Python Execution (pyodide-worker.js)               │
│ - Catches: Python errors, AST validation errors             │
│ - Action: Format friendly error message                     │
└──────────────────────┬──────────────────────────────────────┘
                       │ Runtime Error
                       ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Error Handler (errorHandler.js)                    │
│ - Transforms all error types into beginner-friendly messages│
│ - Shows code context, hints, and next steps                 │
└─────────────────────────────────────────────────────────────┘
```

**Key Points:**
- Security errors get special friendly messages (not punishment language)
- Timeout errors suggest reducing loop iterations or simplifying code
- Import restriction errors suggest allowed alternatives
- Canvas size errors explain the limit and suggest smaller sizes

---

## Phase 1: Foundation (1-2 days)

### 1.0 Prerequisites

**Dependencies on Security Implementation:**
- Requires `executor.js` for worker management and timeout handling
- Requires `pyodide-worker.js` enhancements for Python-side error formatting
- Works with `validator.js` for pre-execution validation errors

If security implementation is not complete, error handling can still be implemented with basic try-catch, but will lack:
- Timeout error handling
- Pre-validation error messages
- Worker crash recovery

### 1.1 Create Error Handler Module

Create `errorHandler.js` with a class that:
- Initializes Python error formatting functions
- Catches Pyodide errors
- Transforms technical messages into beginner-friendly ones
- Extracts code snippets and line numbers

```javascript
// errorHandler.js
class PyodideErrorHandler {
    constructor(pyodide) {
        this.pyodide = pyodide;
    }
    
    async init() {
        // Set up Python error formatter
        await this.pyodide.runPythonAsync(`
            import sys
            from traceback import extract_tb
            
            def get_error_info():
                if not hasattr(sys, 'last_type'):
                    return None
                
                exc_type = sys.last_type
                exc_value = sys.last_value
                exc_tb = sys.last_traceback
                
                # Get user code frames only (filter Pyodide internals)
                tb_list = extract_tb(exc_tb)
                user_frames = [f for f in tb_list 
                              if '/lib/python' not in f.filename]
                
                line_no = user_frames[-1].lineno if user_frames else None
                
                return {
                    'type': exc_type.__name__,
                    'message': str(exc_value),
                    'line': line_no
                }
        `);
    }
    
    async handleError(error, userCode) {
        const info = this.pyodide.globals.get("get_error_info")();
        if (!info) return this.formatGenericError(error);
        
        const data = info.toJs();
        return this.formatForBeginners(data, userCode);
    }
    
    formatForBeginners(errorData, code) {
        const { type, message, line } = errorData;
        
        return {
            title: this.getTitle(type),
            explanation: this.getExplanation(type, message),
            hint: this.getHint(type, message),
            line: line,
            snippet: this.getSnippet(code, line)
        };
    }
    
    getTitle(type) {
        const titles = {
            // Python errors
            'SyntaxError': 'Syntax Problem',
            'NameError': 'Variable Not Found',
            'TypeError': 'Wrong Type',
            'IndentationError': 'Indentation Problem',
            'IndexError': 'List Index Problem',
            'AttributeError': 'Attribute Not Found',
            
            // Security errors
            'ValidationError': 'Code Not Allowed',
            'TimeoutError': 'Code Taking Too Long',
            'ImportError': 'Import Not Allowed',
            'ValueError': 'Invalid Value',
            
            // System errors
            'WorkerError': 'System Problem'
        };
        return titles[type] || 'Error';
    }
    
    getExplanation(type, message) {
        // Python errors
        if (type === 'SyntaxError') {
            return 'Python doesn\'t understand this code. Check for missing colons, quotes, or brackets.';
        }
        if (type === 'NameError') {
            const match = message.match(/name '(\w+)' is not defined/);
            const varName = match ? match[1] : 'this variable';
            return `You used ${varName} but haven't created it yet.`;
        }
        if (type === 'TypeError') {
            return 'You\'re trying to use values in a way that doesn\'t work together.';
        }
        if (type === 'IndentationError') {
            return 'The spacing at the start of this line is wrong.';
        }
        if (type === 'IndexError') {
            return 'You tried to access an item that doesn\'t exist in your list.';
        }
        
        // Security errors
        if (type === 'TimeoutError' || message.includes('timeout')) {
            return 'Your code is taking too long to run. It might have an infinite loop or too many shapes.';
        }
        if (type === 'ImportError' && message.includes('not allowed')) {
            return 'This import is not available in the drawing environment.';
        }
        if (type === 'ValidationError') {
            return 'This code uses features that aren\'t allowed for safety reasons.';
        }
        if (type === 'ValueError' && message.includes('Canvas')) {
            return 'Your canvas size is too large. Try using smaller dimensions.';
        }
        if (message.includes('Shape limit exceeded')) {
            return 'You\'re trying to draw too many shapes. Try reducing your loop iterations.';
        }
        
        return message;
    }
    
    getHint(type, message) {
        // Python error hints
        if (type === 'NameError') {
            const match = message.match(/name '(\w+)' is not defined/);
            if (match) {
                return `Try adding: ${match[1]} = ... before using it`;
            }
        }
        if (type === 'SyntaxError' && message.includes('EOL')) {
            return 'Did you forget to close a quote?';
        }
        if (type === 'IndentationError') {
            return 'Make sure all lines at the same level have the same spacing';
        }
        if (type === 'IndexError') {
            return 'Remember: lists start counting at 0';
        }
        
        // Security error hints
        if (type === 'TimeoutError' || message.includes('timeout')) {
            return 'Try: Use smaller numbers in range(), reduce loop iterations, or simplify your drawing';
        }
        if (type === 'ImportError' && message.includes('not allowed')) {
            const match = message.match(/Import '(\w+)' not allowed/);
            if (match) {
                return `Only Canvas and Color can be imported. Remove: import ${match[1]}`;
            }
            return 'Only Canvas and Color imports are available in this environment';
        }
        if (message.includes('Canvas width') || message.includes('Canvas height')) {
            return 'Try: Canvas(800, 600) - Maximum size is 2000x2000 pixels';
        }
        if (message.includes('Shape limit')) {
            return 'Try: Reduce your range() number or use fewer drawing commands';
        }
        if (message.includes('Forbidden pattern')) {
            return 'This code uses advanced features not available in the learning environment';
        }
        
        return null;
    }
    
    getSnippet(code, lineNumber, context = 2) {
        if (!code || !lineNumber) return null;
        
        const lines = code.split('\n');
        const start = Math.max(0, lineNumber - context - 1);
        const end = Math.min(lines.length, lineNumber + context);
        
        return lines.slice(start, end).map((line, idx) => ({
            number: start + idx + 1,
            code: line,
            isError: start + idx + 1 === lineNumber
        }));
    }
    
    formatGenericError(error) {
        return {
            title: 'Something Went Wrong',
            explanation: error.message,
            hint: null,
            line: null,
            snippet: null
        };
    }
}
```

### 1.2 Integrate with Security Executor

The error handler works with the security system's executor:

```javascript
// Import security components (from SECURITY_IMPLEMENTATION_PLAN.md)
import { CodeValidator } from './js/security/validator.js';
import { executor } from './js/security/executor.js';
import { PyodideErrorHandler } from './errorHandler.js';

// Initialize error handler once Pyodide is ready
let errorHandler;
executor.waitForReady().then(() => {
    errorHandler = new PyodideErrorHandler(executor.worker.pyodide);
    errorHandler.init();
});

async function runUserCode(code) {
    // Step 1: Pre-validation (catches security issues before execution)
    const validation = CodeValidator.validate(code);
    if (!validation.valid) {
        return {
            success: false,
            error: errorHandler.formatValidationError(validation.errors)
        };
    }
    
    // Step 2: Execute with timeout protection
    try {
        const result = await executor.execute(code);
        return { success: true, result };
    } catch (error) {
        // Step 3: Format error based on type
        let friendly;
        
        if (error.message.includes('timeout')) {
            // Timeout from executor.js
            friendly = errorHandler.formatTimeoutError(error);
        } else if (error.message.includes('Worker crashed')) {
            // Worker crash
            friendly = errorHandler.formatSystemError(error);
        } else {
            // Python execution error
            friendly = await errorHandler.handleError(error, code);
        }
        
        return { success: false, error: friendly };
    }
}
```

**Add formatting methods for security errors:**

```javascript
// Add to PyodideErrorHandler class

formatValidationError(errors) {
    // Pre-validation caught the error before execution
    const firstError = errors[0];
    
    return {
        title: 'Code Not Allowed',
        explanation: this.getSecurityExplanation(firstError),
        hint: this.getSecurityHint(firstError),
        line: this.extractLineNumber(firstError),
        snippet: null,
        category: 'security'
    };
}

formatTimeoutError(error) {
    return {
        title: 'Code Taking Too Long',
        explanation: 'Your code ran for more than 5 seconds. It might have an infinite loop or be drawing too many shapes.',
        hint: 'Try: Reduce range() numbers, simplify your loops, or draw fewer shapes',
        line: null,
        snippet: null,
        category: 'timeout'
    };
}

formatSystemError(error) {
    return {
        title: 'System Problem',
        explanation: 'Something went wrong with the code runner. Try running your code again.',
        hint: 'If this keeps happening, try refreshing the page',
        line: null,
        snippet: null,
        category: 'system'
    };
}

getSecurityExplanation(errorMessage) {
    if (errorMessage.includes('Import')) {
        return 'Only Canvas and Color can be imported in this environment.';
    }
    if (errorMessage.includes('Canvas')) {
        return 'Canvas size is too large. Maximum size is 2000×2000 pixels.';
    }
    if (errorMessage.includes('large number')) {
        return 'You\'re using very large numbers that might slow down or crash the browser.';
    }
    if (errorMessage.includes('Forbidden pattern')) {
        return 'This code uses features that aren\'t available for safety reasons.';
    }
    return 'This code cannot be run in the learning environment.';
}

getSecurityHint(errorMessage) {
    if (errorMessage.includes('Canvas width') || errorMessage.includes('Canvas height')) {
        return 'Try: Canvas(800, 600) instead';
    }
    if (errorMessage.includes('Import') && errorMessage.includes('not allowed')) {
        return 'Remove the import line - Canvas and Color are already available';
    }
    if (errorMessage.includes('large number')) {
        return 'Use smaller numbers in range() - try range(100) instead of range(1000000)';
    }
    return null;
}

extractLineNumber(errorMessage) {
    // Try to extract line number from validation error
    const match = errorMessage.match(/line (\d+)/i);
    return match ? parseInt(match[1]) : null;
}
```

---

## Phase 2: UI Components (1 day)

### 2.1 Error Display Component

Create a React component that displays errors in a friendly format with category-based styling:

```javascript
function ErrorMessage({ error, onDismiss }) {
    // Determine CSS class based on error category
    const categoryClass = error.category 
        ? `${error.category}-error` 
        : 'python-error';
    
    // Choose icon based on category
    const icons = {
        python: '⚠️',
        security: 'ℹ️',
        timeout: '⏱️',
        system: '⚙️'
    };
    const icon = icons[error.category] || '⚠️';
    
    return (
        <div className={`error-card ${categoryClass}`}>
            <div className="error-header">
                <span className="error-icon">{icon}</span>
                <h3>{error.title}</h3>
                <button onClick={onDismiss} className="close-btn" aria-label="Dismiss error">×</button>
            </div>
            
            <p className="error-explanation">{error.explanation}</p>
            
            {error.hint && (
                <div className="error-hint">
                    <span className="hint-icon">💡</span>
                    <span>{error.hint}</span>
                </div>
            )}
            
            {error.snippet && (
                <div className="error-code">
                    {error.snippet.map(line => (
                        <div 
                            key={line.number}
                            className={line.isError ? 'code-line error-line' : 'code-line'}
                        >
                            <span className="line-number">{line.number}</span>
                            <span className="line-code">{line.code}</span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
```

### 2.2 Error Styling

Create CSS for the error display with visual distinction for error types:

```css
/* Base error card */
.error-card {
    border-radius: 4px;
    padding: 16px;
    margin: 16px 0;
    font-family: system-ui, -apple-system, sans-serif;
}

/* Python errors - Orange/Yellow theme (learning opportunity) */
.error-card.python-error {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
}

.error-card.python-error .error-header h3 {
    color: #E65100;
}

/* Security errors - Blue theme (information, not punishment) */
.error-card.security-error {
    background: #E3F2FD;
    border-left: 4px solid #2196F3;
}

.error-card.security-error .error-header h3 {
    color: #1565C0;
}

/* Timeout errors - Purple theme (performance issue) */
.error-card.timeout-error {
    background: #F3E5F5;
    border-left: 4px solid #9C27B0;
}

.error-card.timeout-error .error-header h3 {
    color: #6A1B9A;
}

/* System errors - Gray theme (technical issue) */
.error-card.system-error {
    background: #FAFAFA;
    border-left: 4px solid #757575;
}

.error-card.system-error .error-header h3 {
    color: #424242;
}

.error-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
}

.error-icon {
    font-size: 24px;
}

.error-header h3 {
    flex: 1;
    margin: 0;
    font-size: 18px;
}

.close-btn {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #666;
}

.error-explanation {
    color: #333;
    margin: 0 0 12px 0;
    font-size: 15px;
}

.error-hint {
    background: #FFF9C4;
    border-radius: 4px;
    padding: 8px 12px;
    display: flex;
    gap: 8px;
    align-items: start;
    margin-bottom: 12px;
}

.hint-icon {
    font-size: 18px;
}

.error-code {
    background: #F5F5F5;
    border-radius: 4px;
    padding: 8px;
    font-family: 'Monaco', 'Consolas', monospace;
    font-size: 13px;
    overflow-x: auto;
}

.code-line {
    display: flex;
    gap: 12px;
    padding: 2px 4px;
}

.error-line {
    background: #FFCDD2;
    margin: 0 -4px;
    padding: 2px 4px;
}

.line-number {
    color: #999;
    width: 30px;
    text-align: right;
    user-select: none;
}

.line-code {
    white-space: pre;
}
```

**Key Design Decisions:**
- **Orange/Yellow** for Python errors = "This is a learning opportunity"
- **Blue** for security errors = "This is information, not punishment"
- **Purple** for timeouts = "This is a performance issue"
- **Gray** for system errors = "This is our problem, not yours"

### 2.3 Code Editor Enhancement

Add visual error indicators in the code editor:

```javascript
function CodeEditor({ value, onChange, errorLine }) {
    return (
        <div className="editor-container">
            <div className="line-numbers">
                {value.split('\n').map((_, idx) => (
                    <div 
                        key={idx}
                        className={idx + 1 === errorLine ? 'line-number error' : 'line-number'}
                    >
                        {idx + 1 === errorLine && '❌ '}
                        {idx + 1}
                    </div>
                ))}
            </div>
            <textarea 
                value={value}
                onChange={e => onChange(e.target.value)}
                spellCheck={false}
            />
        </div>
    );
}
```

---

## Phase 3: Curriculum-Specific Enhancements (1-2 days)

### 3.1 Lesson-Aware Error Messages

Enhance error handler with lesson context:

```javascript
getDrawingHint(type, message, lessonContext) {
    // Lesson 1-2: Variables and shapes
    if (lessonContext.lesson <= 2) {
        if (type === 'NameError') {
            return 'Remember to set your variable first: width = 200';
        }
        if (type === 'TypeError' && message.includes('rect')) {
            return 'canvas.rect() needs: x, y, width, height';
        }
    }
    
    // Lesson 6+: Loops
    if (lessonContext.lesson >= 6 && type === 'IndentationError') {
        return 'Code inside the for loop must be indented (4 spaces)';
    }
    
    // Lesson 11+: Functions
    if (lessonContext.lesson >= 11) {
        if (type === 'TypeError' && message.includes('argument')) {
            return 'Check your function definition - does it have the right parameters?';
        }
    }
    
    return null;
}
```

### 3.2 Canvas API Limit Errors

Handle errors from Canvas size and shape limits (from shapes.py modifications):

```javascript
// Add to getExplanation method
if (message.includes('Canvas width') && message.includes('exceeds maximum')) {
    return 'Your canvas is too wide. The maximum width is 2000 pixels.';
}
if (message.includes('Canvas height') && message.includes('exceeds maximum')) {
    return 'Your canvas is too tall. The maximum height is 2000 pixels.';
}
if (message.includes('Canvas area') && message.includes('exceeds maximum')) {
    return 'Your canvas is too large overall. Try smaller dimensions.';
}
if (message.includes('Shape limit exceeded')) {
    const match = message.match(/\((\d+)\)/);
    const limit = match ? match[1] : '10,000';
    return `You're trying to draw too many shapes (limit is ${limit}). This can crash the browser.`;
}

// Add to getHint method
if (message.includes('Canvas width') || message.includes('Canvas height')) {
    return 'Try: Canvas(800, 600) - this is a good size for most drawings';
}
if (message.includes('Shape limit')) {
    return 'Try: Reduce your range() number. For example, change range(20000) to range(100)';
}
```

**Error message examples:**

```javascript
// Canvas too large
{
    title: 'Canvas Too Large',
    explanation: 'Your canvas is too wide. The maximum width is 2000 pixels.',
    hint: 'Try: Canvas(800, 600) - this is a good size for most drawings',
    line: 1,
    snippet: [
        { number: 1, code: 'can = Canvas(5000, 600)', isError: true }
    ]
}

// Too many shapes
{
    title: 'Too Many Shapes',
    explanation: 'You\'re trying to draw too many shapes (limit is 10,000). This can crash the browser.',
    hint: 'Try: Reduce your range() number. For example, change range(20000) to range(100)',
    line: 3,
    snippet: [
        { number: 2, code: 'for i in range(20000):', isError: false },
        { number: 3, code: '    can.circle(i, 300, 10)', isError: true }
    ]
}
```

Add specific messages for drawing API errors:

```javascript
getCanvasErrorHint(message) {
    if (message.includes('Canvas')) {
        return 'Did you create the canvas first? Use: can = Canvas(800, 600)';
    }
    if (message.includes('rect')) {
        return 'canvas.rect() needs 4 numbers: x, y, width, height';
    }
    if (message.includes('circle')) {
        return 'canvas.circle() needs 3 numbers: x, y, radius';
    }
    if (message.includes('Color')) {
        return 'Use Color.RED, Color.BLUE, etc., or a hex color like "#FF0000"';
    }
    return null;
}
```

---

## Phase 4: Testing & Refinement (1 day)

### 4.1 Test Common Beginner Errors

Create test suite with typical student errors:

```javascript
const testCases = [
    // Syntax errors
    {
        code: 'can = Canvas(800, 600\ncan.rect(100, 100, 50, 50)',
        description: 'Missing closing parenthesis'
    },
    {
        code: 'can.rect(100, 100, 50, 50 fill=Color.RED)',
        description: 'Missing comma between arguments'
    },
    {
        code: 'width = 200\nheight = 100\ncan.rect(x, y, width height)',
        description: 'Missing comma in arguments'
    },
    
    // Name errors
    {
        code: 'can.rect(x, y, 50, 50)',
        description: 'Undefined variables'
    },
    {
        code: 'width = 200\ncan.rect(100, 100, widht, 100)',
        description: 'Typo in variable name'
    },
    
    // Type errors
    {
        code: 'can.rect("100", 100, 50, 50)',
        description: 'String instead of number'
    },
    {
        code: 'can.rect(100 + "50", 100, 50, 50)',
        description: 'Cannot add number and string'
    },
    
    // Indentation errors
    {
        code: 'for i in range(5):\ncan.rect(i*50, 100, 40, 40)',
        description: 'Missing indentation in loop'
    },
    {
        code: 'for i in range(5):\n    can.rect(i*50, 100, 40, 40)\n  can.circle(i*50, 100, 20)',
        description: 'Inconsistent indentation'
    },
    
    // Security errors - Validation layer
    {
        code: 'import os\ncan = Canvas(800, 600)',
        description: 'Forbidden import (pre-validation)',
        expectValidationError: true
    },
    {
        code: 'can = Canvas(5000, 5000)',
        description: 'Canvas too large (pre-validation)',
        expectValidationError: true
    },
    {
        code: 'for i in range(10000000):\n    print(i)',
        description: 'Suspicious large number (pre-validation)',
        expectValidationError: true
    },
    
    // Security errors - Runtime layer
    {
        code: 'can = Canvas(800, 600)\nfor i in range(15000):\n    can.circle(i, 300, 10)',
        description: 'Too many shapes (runtime)',
        expectRuntimeError: true
    },
    {
        code: 'while True:\n    pass',
        description: 'Infinite loop (timeout)',
        expectTimeout: true
    },
    
    // Canvas API errors
    {
        code: 'can = Canvas(3000, 600)',
        description: 'Canvas width exceeds limit (Python)',
        expectRuntimeError: true
    },
    {
        code: 'can = Canvas(800, 3000)',
        description: 'Canvas height exceeds limit (Python)',
        expectRuntimeError: true
    },
];

// Run tests
async function runErrorTests() {
    console.log('=== Error Handling Test Suite ===\n');
    
    let passed = 0;
    let failed = 0;
    
    for (const test of testCases) {
        console.log(`\n[${test.description}]`);
        console.log(`Code: ${test.code.substring(0, 50)}${test.code.length > 50 ? '...' : ''}`);
        
        const result = await runUserCode(test.code);
        
        if (!result.success) {
            console.log('✓ Error caught');
            console.log(`  Title: ${result.error.title}`);
            console.log(`  Explanation: ${result.error.explanation}`);
            console.log(`  Hint: ${result.error.hint || 'None'}`);
            console.log(`  Category: ${result.error.category || 'python'}`);
            
            // Verify expected error type
            if (test.expectValidationError && result.error.category !== 'security') {
                console.log('✗ FAIL: Expected validation error');
                failed++;
            } else if (test.expectTimeout && result.error.category !== 'timeout') {
                console.log('✗ FAIL: Expected timeout error');
                failed++;
            } else {
                passed++;
            }
        } else {
            console.log('✗ FAIL: No error caught');
            failed++;
        }
    }
    
    console.log(`\n=== Results: ${passed} passed, ${failed} failed ===`);
}
```

**Integration test with security layers:**

```javascript
async function testSecurityIntegration() {
    console.log('=== Testing Security Layer Integration ===\n');
    
    // Test 1: Pre-validation catches forbidden import
    console.log('Test 1: Forbidden import (should be caught by validator)');
    let result = await runUserCode('import os');
    assert(result.error.category === 'security', 'Should catch at validation layer');
    console.log('✓ Pass\n');
    
    // Test 2: Timeout protection
    console.log('Test 2: Infinite loop (should timeout after 5s)');
    const start = Date.now();
    result = await runUserCode('while True:\n    pass');
    const duration = Date.now() - start;
    assert(result.error.category === 'timeout', 'Should detect timeout');
    assert(duration >= 4900 && duration <= 5500, 'Should timeout at ~5 seconds');
    console.log(`✓ Pass (timed out in ${duration}ms)\n`);
    
    // Test 3: Canvas size limit (Python runtime)
    console.log('Test 3: Canvas too large (should be caught by shapes.py)');
    result = await runUserCode('can = Canvas(3000, 600)');
    assert(!result.success, 'Should fail');
    assert(result.error.explanation.includes('too wide'), 'Should explain size issue');
    console.log('✓ Pass\n');
    
    // Test 4: Shape count limit (Python runtime)
    console.log('Test 4: Too many shapes (should be caught by shapes.py)');
    result = await runUserCode('can = Canvas(800, 600)\nfor i in range(15000):\n    can.circle(i, 300, 10)');
    assert(!result.success, 'Should fail');
    assert(result.error.explanation.includes('too many'), 'Should explain shape limit');
    console.log('✓ Pass\n');
    
    console.log('=== All security integration tests passed ===');
}
```

### 4.2 Validate Error Messages

Ensure messages are:
- [ ] Clear and concise (under 100 characters)
- [ ] Use student-appropriate vocabulary
- [ ] Avoid technical jargon
- [ ] Provide actionable hints
- [ ] Show relevant code context

---

## Implementation Checklist

### Prerequisites
- [ ] Security implementation complete (executor.js, validator.js, pyodide-worker.js)
- [ ] Canvas size limits added to shapes.py
- [ ] Web worker architecture operational

### Core Implementation
- [ ] Create `errorHandler.js` module
- [ ] Add Python error formatting function
- [ ] Add security error formatting methods
- [ ] Initialize error handler with Pyodide
- [ ] Integrate with security executor
- [ ] Test basic error catching works

### Security Integration
- [ ] Handle pre-validation errors from validator.js
- [ ] Handle timeout errors from executor.js
- [ ] Handle Canvas size limit errors from shapes.py
- [ ] Handle shape count limit errors from shapes.py
- [ ] Test error messages for forbidden imports
- [ ] Test error messages for canvas size violations
- [ ] Test error messages for timeout scenarios

### UI Components
- [ ] Create `ErrorMessage` component
- [ ] Add error styling CSS
- [ ] Add visual distinction for security errors
- [ ] Integrate error display in main UI
- [ ] Add error icon and visual hierarchy
- [ ] Test error display with mock data

### Code Editor Integration
- [ ] Add line highlighting in editor
- [ ] Show error indicator on problem line
- [ ] Test line number accuracy
- [ ] Handle multi-line code properly

### Error Messages
- [ ] Add beginner-friendly titles for Python errors
- [ ] Add beginner-friendly titles for security errors
- [ ] Write clear explanations
- [ ] Create helpful hints
- [ ] Test with common errors from lessons 1-5
- [ ] Add drawing-specific messages

### Lesson-Specific Features
- [ ] Add lesson context to error handler
- [ ] Create lesson-aware hints
- [ ] Test errors for lessons 6-10 (loops)
- [ ] Test errors for lessons 11-15 (functions)

### Testing & Polish
- [ ] Run all Python error test cases
- [ ] Run all security error test cases
- [ ] Run security integration test suite
- [ ] Verify error messages with students (if possible)
- [ ] Add error dismissal functionality
- [ ] Test on mobile devices
- [ ] Add keyboard accessibility (ESC to dismiss)

---

## Key Design Principles

### 1. Start Simple
Begin with basic friendly messages. Add sophistication only after core functionality works.

### 2. Show Code Context
Always highlight the problem line and show surrounding code for context.

### 3. Provide Hints
Don't just explain what went wrong—suggest how to fix it.

### 4. Progressive Disclosure
Start with simple message. Make technical details available but hidden by default.

### 5. Match Curriculum
Use terminology and concepts from the student's current lesson level.

### 6. Visual Hierarchy
Use color, icons, and spacing to communicate:
- **Orange/Yellow** = Learning opportunity (Python errors)
- **Blue** = Information (security restrictions)
- **Purple** = Performance issue (timeouts)
- **Gray** = System issue

### 7. Security Error Language
Security errors require special consideration:
- **Never use punishment language** ("You violated...", "You're not allowed...")
- **Frame as helpful limits** ("To keep things running smoothly...", "This helps prevent...")
- **Suggest alternatives** (Don't just say no—show what they CAN do)
- **Be educational** (Explain WHY the limit exists)

**Examples:**

❌ Bad:
```
"Import 'os' is forbidden. You violated security policy."
```

✅ Good:
```
"Only Canvas and Color can be imported in this environment.
💡 These are already available - no import needed!"
```

❌ Bad:
```
"Canvas size exceeds maximum. Access denied."
```

✅ Good:
```
"Canvas size is too large. Maximum size is 2000×2000 pixels.
💡 Try: Canvas(800, 600) - this is a good size for most drawings"
```

---

## Common Error Categories

### Python Errors (Lessons 1-5)

#### Syntax Errors
- Missing colons after `if`, `for`, `def`
- Unclosed quotes or brackets
- Missing commas between arguments

#### Name Errors
- Using undefined variables
- Typos in variable names
- Using variables before defining them

#### Type Errors (Lessons 2-7)
- Wrong argument types to functions
- Incompatible operations (string + number)
- Wrong number of arguments

### Python Errors (Lessons 6+)

#### Indentation Errors
- Missing indentation in loops
- Inconsistent indentation
- Mixing tabs and spaces

#### Index Errors (Lessons 7+)
- Accessing list items that don't exist
- Off-by-one errors

### Security Errors (All Lessons)

#### Pre-Validation Errors
Caught by `validator.js` before execution:
- **Forbidden imports** - Only Canvas and Color allowed
- **Canvas too large** - Maximum 2000×2000 pixels
- **Suspicious large numbers** - Prevents DoS attempts
- **Forbidden patterns** - Blocks eval, exec, etc.

**Message style:** Informative, educational
**Action:** Show alternative or explain why restricted

#### Runtime Security Errors
Caught during Python execution:
- **Canvas size exceeded** - From shapes.py validation
- **Shape limit exceeded** - Too many drawing commands (>10,000)
- **Import error** - Tried to import restricted module

**Message style:** Helpful, solution-focused
**Action:** Suggest fix or smaller values

#### Performance Errors
Caught by `executor.js`:
- **Timeout** - Code ran longer than 5 seconds
- **Worker crash** - Severe error crashed execution environment

**Message style:** Problem-solving, not blaming
**Action:** Suggest reducing iterations or simplifying code

---

## Future Enhancements

After basic implementation is complete, consider:

### Analytics
- Track which errors students hit most frequently
- Identify confusing error messages that need improvement
- Generate lesson-specific error reports

### Interactive Help
- Add "Try this instead" quick fixes
- Inline tutorials for common errors
- Video explanations for complex concepts

### Advanced Features
- AI-powered error explanations
- "Ask for help" button that formats error for sharing
- Error history to see past mistakes
- Achievement system for fixing errors independently

---

## Success Metrics

Implementation is successful when:

### Understanding
- Students understand what went wrong (>80% comprehension)
- Students understand why security limits exist (>70% comprehension)
- Students distinguish between code errors and safety limits

### Problem-Solving
- Students know how to fix Python errors (>70% can fix without help)
- Students can adjust code to work within security limits (>80% success rate)
- Students reference error hints in their fixes (observable behavior)

### User Experience
- Error messages reduce frustration (subjective feedback)
- Students don't feel punished by security restrictions (subjective feedback)
- Technical tracebacks are rarely needed (>90% resolved with friendly message)

### Security-Specific Metrics
- Pre-validation catches dangerous code before execution (100% of test cases)
- Timeout protection prevents browser freezes (100% of infinite loops)
- Canvas size limits prevent browser crashes (100% of oversized canvases)
- Students successfully modify code after security errors (>75% success rate)
- Security error messages perceived as helpful, not punitive (subjective feedback)

### System Reliability
- Worker crashes don't lose student work (<1% data loss)
- Error handler never crashes (0 handler failures)
- All error types have friendly messages (100% coverage)

---

## Resources

- Pyodide documentation: https://pyodide.org/
- UX error message guidelines: https://www.nngroup.com/articles/error-message-guidelines/
- Python error types: https://docs.python.org/3/library/exceptions.html
- Friendly-Traceback project: https://friendly-traceback.github.io/
- Security Implementation Plan: SECURITY_IMPLEMENTATION_PLAN.md

---

## Implementation Order

This error handling plan integrates with the security implementation. Recommended implementation sequence:

### Option 1: Security First (Recommended)
1. Complete security implementation (SECURITY_IMPLEMENTATION_PLAN.md Phases 1-4)
2. Test security layers work (validation, timeout, restrictions)
3. Implement error handling (this plan Phases 1-2)
4. Integrate error handling with security (this plan Phase 1.2)
5. Test complete system (this plan Phase 4)

**Advantage:** Error handling can properly handle all error types from the start

### Option 2: Parallel Implementation
1. Implement basic error handling (this plan Phase 1.1, 2)
2. Implement security foundation (SECURITY_IMPLEMENTATION_PLAN.md Phases 1-3)
3. Integrate error handling with security (this plan Phase 1.2)
4. Complete both systems (remaining phases)

**Advantage:** Faster overall implementation

### Option 3: Error Handling First
1. Implement basic error handling (this plan Phases 1-2)
2. Test with basic Pyodide execution
3. Implement security (SECURITY_IMPLEMENTATION_PLAN.md)
4. Update error handler for security errors (this plan Phase 1.2)

**Advantage:** Students see friendly errors sooner, but will need updates later

**Recommendation:** Use Option 1 (Security First) for cleanest implementation and minimal rework.

---

## Coordination Points

These areas require coordination between security and error handling:

### 1. Worker Architecture
- **Security provides:** Web worker with execution isolation
- **Error handling needs:** Access to Pyodide instance for error formatting
- **Integration point:** Pass Pyodide reference to error handler after initialization

### 2. Timeout Handling
- **Security provides:** 5-second timeout with worker termination
- **Error handling needs:** Friendly timeout message
- **Integration point:** Catch timeout exception and format message

### 3. Validation Errors
- **Security provides:** Pre-execution code validation
- **Error handling needs:** Format validation errors for display
- **Integration point:** `formatValidationError()` method in error handler

### 4. Canvas Limits
- **Security provides:** Size limits in shapes.py
- **Error handling needs:** Explain limits helpfully
- **Integration point:** Detect ValueError with canvas-related message

### 5. AST Validation
- **Security provides:** Python AST analysis of forbidden patterns
- **Error handling needs:** Translate technical violations to learning moments
- **Integration point:** Detect ImportError or ValidationError from Python

---

## Notes

- Keep error messages under 100 characters when possible
- Always test with actual students if available
- Prioritize the most common errors first
- Update messages based on student feedback
- Consider internationalization for multi-language support