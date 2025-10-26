# Error Handling Implementation Plan
## Python Drawing Curriculum - Friendly Error Messages

---

## Overview

This plan implements beginner-friendly error messages for the Python drawing curriculum. When students write code that causes errors, they'll see clear explanations, helpful hints, and visual indicators instead of technical Python tracebacks.

**Goal:** Transform frustrating error experiences into learning opportunities that guide students toward solutions.

---

## Phase 1: Foundation (1-2 days)

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
            'SyntaxError': 'Syntax Problem',
            'NameError': 'Variable Not Found',
            'TypeError': 'Wrong Type',
            'IndentationError': 'Indentation Problem',
            'IndexError': 'List Index Problem',
            'AttributeError': 'Attribute Not Found'
        };
        return titles[type] || 'Error';
    }
    
    getExplanation(type, message) {
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
        return message;
    }
    
    getHint(type, message) {
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

### 1.2 Integrate into Code Execution

Wrap your code runner with error handling:

```javascript
// In your code runner module
const errorHandler = new PyodideErrorHandler(pyodide);
await errorHandler.init();

async function runUserCode(code) {
    try {
        const result = await pyodide.runPythonAsync(code);
        return { success: true, result };
    } catch (error) {
        const friendly = await errorHandler.handleError(error, code);
        return { success: false, error: friendly };
    }
}
```

---

## Phase 2: UI Components (1 day)

### 2.1 Error Display Component

Create a React component that displays errors in a friendly format:

```javascript
function ErrorMessage({ error, onDismiss }) {
    return (
        <div className="error-card">
            <div className="error-header">
                <span className="error-icon">⚠️</span>
                <h3>{error.title}</h3>
                <button onClick={onDismiss} className="close-btn">×</button>
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

Create CSS for the error display:

```css
.error-card {
    background: #FFF3E0;
    border-left: 4px solid #FF9800;
    border-radius: 4px;
    padding: 16px;
    margin: 16px 0;
    font-family: system-ui, -apple-system, sans-serif;
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
    color: #E65100;
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

### 3.2 Common Drawing Error Messages

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
];

// Run tests
async function runErrorTests() {
    for (const test of testCases) {
        console.log(`\nTest: ${test.description}`);
        const result = await runUserCode(test.code);
        if (!result.success) {
            console.log('Title:', result.error.title);
            console.log('Explanation:', result.error.explanation);
            console.log('Hint:', result.error.hint);
        }
    }
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

### Core Implementation
- [ ] Create `errorHandler.js` module
- [ ] Add Python error formatting function
- [ ] Initialize error handler with Pyodide
- [ ] Wrap code execution in try-catch
- [ ] Test basic error catching works

### UI Components
- [ ] Create `ErrorMessage` component
- [ ] Add error styling CSS
- [ ] Integrate error display in main UI
- [ ] Add error icon and visual hierarchy
- [ ] Test error display with mock data

### Code Editor Integration
- [ ] Add line highlighting in editor
- [ ] Show error indicator on problem line
- [ ] Test line number accuracy
- [ ] Handle multi-line code properly

### Error Messages
- [ ] Add beginner-friendly titles
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
- [ ] Test all error types in test suite
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
- **Orange/Yellow** = Warning/fixable problem
- **Red** = Error that must be fixed
- **Light yellow** = Helpful hint
- **Gray background** = Code snippet

---

## Common Error Categories

### Syntax Errors (Lessons 1-5)
- Missing colons after `if`, `for`, `def`
- Unclosed quotes or brackets
- Missing commas between arguments

### Name Errors (Lessons 1-5)
- Using undefined variables
- Typos in variable names
- Using variables before defining them

### Type Errors (Lessons 2-7)
- Wrong argument types to functions
- Incompatible operations (string + number)
- Wrong number of arguments

### Indentation Errors (Lessons 6+)
- Missing indentation in loops
- Inconsistent indentation
- Mixing tabs and spaces

### Index Errors (Lessons 7+)
- Accessing list items that don't exist
- Off-by-one errors

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
- Students understand what went wrong (>80% comprehension)
- Students know how to fix the error (>70% can fix without help)
- Error messages reduce frustration (subjective feedback)
- Students reference error hints in their fixes (observable behavior)
- Technical tracebacks are rarely needed (>90% of errors resolved with friendly message)

---

## Resources

- Pyodide documentation: https://pyodide.org/
- UX error message guidelines: https://www.nngroup.com/articles/error-message-guidelines/
- Python error types: https://docs.python.org/3/library/exceptions.html
- Friendly-Traceback project: https://friendly-traceback.github.io/

---

## Notes

- Keep error messages under 100 characters when possible
- Always test with actual students if available
- Prioritize the most common errors first
- Update messages based on student feedback
- Consider internationalization for multi-language support