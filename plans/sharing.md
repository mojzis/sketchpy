# Code Sharing Implementation Plan

**Target**: Enable students to share their Python drawings via URL
**Prerequisites**: Security implementation complete (timeout, import whitelist, worker isolation)
**Goal**: Simple, safe sharing without requiring backend storage

---

## Overview

Students create a drawing → Click "Share" → Get URL → Others can view and run it

**Example Flow:**
```
1. Student creates: can = Canvas(800, 600); can.circle(400, 300, 100, fill=Color.RED)
2. Clicks "Share" button
3. Gets: https://yoursite.com/draw#H4sIAAAAAAAAE6tW...
4. Shares link with classmates
5. Classmates click link → Code loads → Confirmation prompt → Run
```

---

## Architecture Decision: Hash Fragment vs Server Storage

### Option A: URL Hash Fragment (Recommended for MVP)

**Pros:**
- No backend needed
- Works immediately with static hosting
- Privacy-preserving (code never hits server logs)
- Offline-capable after first load
- Zero maintenance

**Cons:**
- URL length limit (~2000 chars = ~1500 chars of code after compression)
- Lessons 1-12 fit easily, Lessons 13-15 may exceed
- Can't moderate content
- No analytics on what's shared

**Decision: Start with Hash Fragment**
- Perfect for educational use case
- Students rarely write >1500 chars in beginner lessons
- Can add server storage later if needed

### Option B: Server Storage (Future Enhancement)

```
POST /api/share → {id: "abc123"}
GET /draw/abc123 → Fetch code, display
```

Future consideration if:
- Teachers want to curate/moderate shares
- Need analytics on popular patterns
- Want to support full lesson 15 projects (100+ lines)

---

## Technical Implementation

### Phase 1: Encoding/Decoding (2 hours)

**File**: `static/js/sharing/encoder.js`

```javascript
/**
 * Compress and encode Python code for URL sharing
 * Uses gzip compression + base64 encoding (URL-safe)
 */
export class CodeEncoder {
    /**
     * Encode Python code to URL-safe string
     * @param {string} code - Python code to encode
     * @returns {Promise<string>} Base64-encoded compressed code
     */
    static async encode(code) {
        // 1. Convert string to bytes
        const encoder = new TextEncoder();
        const bytes = encoder.encode(code);
        
        // 2. Compress with gzip (browser native)
        const compressed = await this.compress(bytes);
        
        // 3. Base64 encode (URL-safe variant)
        const base64 = btoa(String.fromCharCode(...new Uint8Array(compressed)))
            .replace(/\+/g, '-')  // URL-safe: + → -
            .replace(/\//g, '_')  // URL-safe: / → _
            .replace(/=+$/, '');  // Remove padding
        
        return base64;
    }
    
    /**
     * Decode URL-safe string back to Python code
     * @param {string} encoded - Base64-encoded compressed code
     * @returns {Promise<string>} Original Python code
     */
    static async decode(encoded) {
        try {
            // 1. Convert URL-safe base64 back to standard
            const base64 = encoded
                .replace(/-/g, '+')
                .replace(/_/g, '/');
            
            // 2. Decode base64
            const binary = atob(base64);
            const bytes = Uint8Array.from(binary, c => c.charCodeAt(0));
            
            // 3. Decompress gzip
            const decompressed = await this.decompress(bytes);
            
            // 4. Convert bytes to string
            const decoder = new TextDecoder();
            return decoder.decode(decompressed);
        } catch (error) {
            throw new Error(`Failed to decode shared code: ${error.message}`);
        }
    }
    
    /**
     * Compress data using gzip (CompressionStream API)
     */
    static async compress(data) {
        const stream = new Response(data).body
            .pipeThrough(new CompressionStream('gzip'));
        return new Uint8Array(await new Response(stream).arrayBuffer());
    }
    
    /**
     * Decompress gzip data (DecompressionStream API)
     */
    static async decompress(data) {
        const stream = new Response(data).body
            .pipeThrough(new DecompressionStream('gzip'));
        return new Uint8Array(await new Response(stream).arrayBuffer());
    }
    
    /**
     * Estimate URL length for code
     * @param {string} code - Python code
     * @returns {Promise<number>} Estimated URL length
     */
    static async estimateUrlLength(code) {
        const encoded = await this.encode(code);
        const baseUrl = window.location.origin + window.location.pathname;
        return baseUrl.length + 1 + encoded.length; // +1 for #
    }
    
    /**
     * Check if code will fit in URL
     * @param {string} code - Python code
     * @returns {Promise<{fits: boolean, urlLength: number, maxLength: number}>}
     */
    static async checkUrlLength(code) {
        const urlLength = await this.estimateUrlLength(code);
        const maxLength = 2000; // Safe browser limit
        
        return {
            fits: urlLength <= maxLength,
            urlLength,
            maxLength
        };
    }
}

// Browser compatibility check
if (!window.CompressionStream) {
    console.warn('CompressionStream not supported - sharing may not work in older browsers');
}
```

**Action for Claude Code:**
- Create `static/js/sharing/encoder.js`
- Uses modern browser APIs (CompressionStream)
- Includes URL length checking

---

### Phase 2: Share UI Components (2 hours)

**File**: `static/js/sharing/share-manager.js`

```javascript
import { CodeEncoder } from './encoder.js';

/**
 * Manages the share UI and link generation
 */
export class ShareManager {
    constructor() {
        this.shareModal = null;
        this.shareUrl = null;
    }
    
    /**
     * Initialize share button and modal
     */
    init() {
        // Will be called from app.js after Alpine loads
        Alpine.data('shareManager', () => ({
            showShareModal: false,
            shareUrl: '',
            shareError: '',
            isGenerating: false,
            copied: false,
            
            async generateShareLink() {
                this.isGenerating = true;
                this.shareError = '';
                this.copied = false;
                
                try {
                    // Get code from editor
                    const code = window.editor.state.doc.toString();
                    
                    // Check length
                    const lengthCheck = await CodeEncoder.checkUrlLength(code);
                    
                    if (!lengthCheck.fits) {
                        this.shareError = `Code too long for URL sharing!\n\n` +
                            `Your code: ${lengthCheck.urlLength} characters\n` +
                            `Maximum: ${lengthCheck.maxLength} characters\n\n` +
                            `Try:\n` +
                            `• Remove comments\n` +
                            `• Shorten variable names\n` +
                            `• Simplify the drawing`;
                        this.showShareModal = true;
                        return;
                    }
                    
                    // Encode code
                    const encoded = await CodeEncoder.encode(code);
                    
                    // Generate URL
                    const baseUrl = window.location.origin + window.location.pathname;
                    this.shareUrl = `${baseUrl}#${encoded}`;
                    
                    // Show modal
                    this.showShareModal = true;
                    
                } catch (error) {
                    this.shareError = `Failed to create share link: ${error.message}`;
                    this.showShareModal = true;
                } finally {
                    this.isGenerating = false;
                }
            },
            
            async copyToClipboard() {
                try {
                    await navigator.clipboard.writeText(this.shareUrl);
                    this.copied = true;
                    setTimeout(() => this.copied = false, 2000);
                } catch (error) {
                    // Fallback for older browsers
                    this.selectAndCopy();
                }
            },
            
            selectAndCopy() {
                const input = this.$refs.shareUrlInput;
                input.select();
                document.execCommand('copy');
                this.copied = true;
                setTimeout(() => this.copied = false, 2000);
            },
            
            closeModal() {
                this.showShareModal = false;
                this.shareUrl = '';
                this.shareError = '';
                this.copied = false;
            }
        }));
    }
}

// Global instance
export const shareManager = new ShareManager();
```

**Action for Claude Code:**
- Create `static/js/sharing/share-manager.js`
- Integrates with Alpine.js for reactive UI
- Handles link generation and clipboard copying

---

### Phase 3: Load Shared Code (2 hours)

**File**: `static/js/sharing/loader.js`

```javascript
import { CodeEncoder } from './encoder.js';
import { CodeValidator } from '../security/validator.js';

/**
 * Handles loading and running shared code from URL hash
 */
export class SharedCodeLoader {
    /**
     * Check if URL contains shared code
     * @returns {boolean}
     */
    static hasSharedCode() {
        return window.location.hash.length > 1;
    }
    
    /**
     * Load shared code from URL hash
     * @returns {Promise<string|null>} Decoded code or null
     */
    static async loadFromUrl() {
        if (!this.hasSharedCode()) {
            return null;
        }
        
        try {
            // Get hash without the # symbol
            const encoded = window.location.hash.substring(1);
            
            // Decode
            const code = await CodeEncoder.decode(encoded);
            
            return code;
        } catch (error) {
            console.error('Failed to load shared code:', error);
            throw new Error(
                'Failed to load shared code.\n\n' +
                'The link may be corrupted or incomplete. ' +
                'Please check the URL and try again.'
            );
        }
    }
    
    /**
     * Initialize shared code loading on page load
     */
    static async init() {
        if (!this.hasSharedCode()) {
            return; // No shared code, normal flow
        }
        
        try {
            // Load code
            const code = await this.loadFromUrl();
            
            if (!code) return;
            
            // Pre-validate (security check)
            const validation = CodeValidator.validate(code);
            
            // Show shared code warning and confirmation
            const shouldRun = await this.showSharedCodeConfirmation(
                code,
                validation
            );
            
            if (!shouldRun) {
                // User declined - clear hash and show starter code
                window.location.hash = '';
                return;
            }
            
            // Load into editor
            this.loadIntoEditor(code);
            
            // Auto-run if validation passed
            if (validation.valid) {
                // Delay to let UI update
                setTimeout(() => {
                    document.getElementById('run-button')?.click();
                }, 500);
            } else {
                // Show validation errors
                Alpine.store('app').error = CodeValidator.formatErrors(validation.errors);
            }
            
        } catch (error) {
            Alpine.store('app').error = error.message;
        }
    }
    
    /**
     * Show confirmation dialog for shared code
     * @param {string} code - The shared code
     * @param {object} validation - Validation result
     * @returns {Promise<boolean>} User's decision
     */
    static async showSharedCodeConfirmation(code, validation) {
        // Use Alpine.js modal
        return new Promise((resolve) => {
            Alpine.store('sharedCodeModal', {
                show: true,
                code: code,
                lineCount: code.split('\n').length,
                charCount: code.length,
                hasErrors: !validation.valid,
                errors: validation.errors,
                
                accept() {
                    this.show = false;
                    resolve(true);
                },
                
                decline() {
                    this.show = false;
                    resolve(false);
                },
                
                viewCode() {
                    // Expand code preview
                    this.showFullCode = true;
                }
            });
        });
    }
    
    /**
     * Load code into CodeMirror editor
     * @param {string} code
     */
    static loadIntoEditor(code) {
        if (!window.editor) {
            console.error('Editor not initialized');
            return;
        }
        
        // Replace editor content
        const transaction = window.editor.state.update({
            changes: {
                from: 0,
                to: window.editor.state.doc.length,
                insert: code
            }
        });
        
        window.editor.dispatch(transaction);
    }
}
```

**Action for Claude Code:**
- Create `static/js/sharing/loader.js`
- Handles URL hash parsing
- Shows confirmation modal
- Integrates with security validator

---

### Phase 4: UI Templates (1 hour)

**File**: `templates/components/share-modal.html` (new component)

```html
<!-- Share Modal -->
<div x-data="shareManager" 
     x-show="showShareModal"
     x-cloak
     class="modal-overlay"
     @click.self="closeModal()">
    
    <div class="modal-content share-modal">
        <div class="modal-header">
            <h2>📤 Share Your Drawing</h2>
            <button @click="closeModal()" class="close-btn">&times;</button>
        </div>
        
        <div class="modal-body">
            <!-- Success State -->
            <div x-show="shareUrl && !shareError" class="share-success">
                <p class="share-instructions">
                    Copy this link to share your drawing with others:
                </p>
                
                <div class="share-url-container">
                    <input 
                        type="text" 
                        x-ref="shareUrlInput"
                        :value="shareUrl"
                        readonly
                        class="share-url-input"
                        @click="$el.select()"
                    />
                    <button 
                        @click="copyToClipboard()"
                        class="copy-btn"
                        :class="{ 'copied': copied }">
                        <span x-show="!copied">📋 Copy</span>
                        <span x-show="copied">✓ Copied!</span>
                    </button>
                </div>
                
                <div class="share-tips">
                    <h4>Sharing Tips:</h4>
                    <ul>
                        <li>Link works on any device with a browser</li>
                        <li>No account needed to view</li>
                        <li>Code is included in the link (not stored on server)</li>
                        <li>Anyone with link can view and modify the code</li>
                    </ul>
                </div>
            </div>
            
            <!-- Error State -->
            <div x-show="shareError" class="share-error">
                <div class="error-icon">⚠️</div>
                <pre x-text="shareError" class="error-message"></pre>
            </div>
            
            <!-- Loading State -->
            <div x-show="isGenerating" class="share-loading">
                <div class="spinner"></div>
                <p>Generating share link...</p>
            </div>
        </div>
        
        <div class="modal-footer">
            <button @click="closeModal()" class="btn btn-secondary">Close</button>
        </div>
    </div>
</div>

<!-- Shared Code Confirmation Modal -->
<div x-data="$store.sharedCodeModal"
     x-show="show"
     x-cloak
     class="modal-overlay">
    
    <div class="modal-content shared-code-modal">
        <div class="modal-header">
            <h2>⚠️ Shared Code</h2>
        </div>
        
        <div class="modal-body">
            <div class="shared-code-warning">
                <p>
                    <strong>You're about to run code shared by another user.</strong>
                </p>
                <p>
                    This code will run in a secure sandbox, but you should still review it first.
                </p>
            </div>
            
            <div class="code-info">
                <div class="info-item">
                    <span class="label">Lines of code:</span>
                    <span class="value" x-text="lineCount"></span>
                </div>
                <div class="info-item">
                    <span class="label">Characters:</span>
                    <span class="value" x-text="charCount"></span>
                </div>
                <div class="info-item" x-show="hasErrors">
                    <span class="label">Security warnings:</span>
                    <span class="value error" x-text="errors.length"></span>
                </div>
            </div>
            
            <!-- Code Preview -->
            <div class="code-preview">
                <h4>Code Preview:</h4>
                <pre x-text="code.substring(0, 300) + (code.length > 300 ? '...' : '')"></pre>
            </div>
            
            <!-- Security Warnings -->
            <div x-show="hasErrors" class="security-warnings">
                <h4>⚠️ Security Issues Detected:</h4>
                <ul>
                    <template x-for="error in errors">
                        <li x-text="error"></li>
                    </template>
                </ul>
                <p class="warning-note">
                    This code has security issues and won't run. 
                    You can view it in the editor but cannot execute it.
                </p>
            </div>
        </div>
        
        <div class="modal-footer">
            <button @click="decline()" class="btn btn-secondary">Cancel</button>
            <button @click="accept()" class="btn btn-primary">
                <span x-show="!hasErrors">Load & Run</span>
                <span x-show="hasErrors">View Code Only</span>
            </button>
        </div>
    </div>
</div>

<style>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 8px;
    max-width: 600px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-header {
    padding: 1.5rem;
    border-bottom: 1px solid #e5e7eb;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
}

.close-btn {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #6b7280;
    padding: 0;
    width: 2rem;
    height: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
}

.modal-body {
    padding: 1.5rem;
}

.modal-footer {
    padding: 1rem 1.5rem;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
}

.share-url-container {
    display: flex;
    gap: 0.5rem;
    margin: 1rem 0;
}

.share-url-input {
    flex: 1;
    padding: 0.75rem;
    border: 1px solid #d1d5db;
    border-radius: 4px;
    font-family: monospace;
    font-size: 0.875rem;
}

.copy-btn {
    padding: 0.75rem 1.5rem;
    background: #3b82f6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    white-space: nowrap;
    transition: background 0.2s;
}

.copy-btn:hover {
    background: #2563eb;
}

.copy-btn.copied {
    background: #10b981;
}

.share-tips {
    background: #f3f4f6;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
}

.share-tips h4 {
    margin: 0 0 0.5rem 0;
}

.share-tips ul {
    margin: 0;
    padding-left: 1.5rem;
}

.share-tips li {
    margin: 0.25rem 0;
}

.share-error {
    text-align: center;
    padding: 2rem;
}

.error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.error-message {
    background: #fee2e2;
    padding: 1rem;
    border-radius: 4px;
    color: #991b1b;
    text-align: left;
    white-space: pre-wrap;
}

.share-loading {
    text-align: center;
    padding: 2rem;
}

.spinner {
    border: 3px solid #f3f4f6;
    border-top: 3px solid #3b82f6;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    animation: spin 1s linear infinite;
    margin: 0 auto 1rem;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.shared-code-warning {
    background: #fef3c7;
    border-left: 4px solid #f59e0b;
    padding: 1rem;
    margin-bottom: 1rem;
}

.code-info {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    margin-bottom: 1rem;
}

.info-item {
    display: flex;
    justify-content: space-between;
    padding: 0.5rem;
    background: #f9fafb;
    border-radius: 4px;
}

.info-item .label {
    font-weight: 600;
}

.info-item .value.error {
    color: #dc2626;
}

.code-preview {
    margin: 1rem 0;
}

.code-preview h4 {
    margin-bottom: 0.5rem;
}

.code-preview pre {
    background: #1f2937;
    color: #f9fafb;
    padding: 1rem;
    border-radius: 4px;
    overflow-x: auto;
    font-size: 0.875rem;
}

.security-warnings {
    background: #fee2e2;
    border-left: 4px solid #dc2626;
    padding: 1rem;
    margin-top: 1rem;
}

.security-warnings h4 {
    color: #991b1b;
    margin-top: 0;
}

.security-warnings ul {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
}

.warning-note {
    margin-top: 1rem;
    font-weight: 600;
    color: #991b1b;
}

.btn {
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s;
}

.btn-primary {
    background: #3b82f6;
    color: white;
}

.btn-primary:hover {
    background: #2563eb;
}

.btn-secondary {
    background: #e5e7eb;
    color: #374151;
}

.btn-secondary:hover {
    background: #d1d5db;
}

[x-cloak] {
    display: none !important;
}
</style>
```

**Action for Claude Code:**
- Create `templates/components/share-modal.html`
- Complete UI for share and confirmation modals
- Styled and responsive

---

### Phase 5: Integration with Main App (1 hour)

**File**: `static/app.js` (modifications)

```javascript
// Add at top with other imports
import { shareManager } from './js/sharing/share-manager.js';
import { SharedCodeLoader } from './js/sharing/loader.js';

// Initialize sharing after Alpine loads
document.addEventListener('alpine:init', () => {
    // Initialize share manager
    shareManager.init();
    
    // Initialize shared code modal store
    Alpine.store('sharedCodeModal', {
        show: false,
        code: '',
        lineCount: 0,
        charCount: 0,
        hasErrors: false,
        errors: []
    });
});

// Load shared code on page load
window.addEventListener('DOMContentLoaded', async () => {
    // Wait for editor to initialize
    await new Promise(resolve => {
        const checkEditor = setInterval(() => {
            if (window.editor) {
                clearInterval(checkEditor);
                resolve();
            }
        }, 100);
    });
    
    // Load shared code if present
    await SharedCodeLoader.init();
});
```

**File**: `templates/lesson.html.jinja` (modifications)

Add share button to sidebar:

```html
<!-- In sidebar, after Run button -->
<button 
    @click="$data.shareManager.generateShareLink()"
    class="btn btn-share"
    :disabled="$data.shareManager.isGenerating">
    <span x-show="!$data.shareManager.isGenerating">🔗 Share</span>
    <span x-show="$data.shareManager.isGenerating">Generating...</span>
</button>

<!-- Include share modal component -->
{% include 'components/share-modal.html' %}
```

**Action for Claude Code:**
- Modify `static/app.js` to import sharing modules
- Modify `templates/lesson.html.jinja` to add share button
- Include modal component

---

### Phase 6: Build Process Updates (30 min)

**File**: `scripts/build.py` (modifications)

```python
def copy_static_files(output_dir):
    """Copy static files to output directory"""
    static_src = Path('static')
    static_dst = output_dir / 'static'
    
    # Create directories
    (static_dst / 'js' / 'security').mkdir(parents=True, exist_ok=True)
    (static_dst / 'js' / 'sharing').mkdir(parents=True, exist_ok=True)
    
    # Copy files
    files_to_copy = [
        'app.js',
        'js/pyodide-worker.js',
        'js/security/config.js',
        'js/security/validator.js',
        'js/security/executor.js',
        'js/sharing/encoder.js',         # NEW
        'js/sharing/share-manager.js',   # NEW
        'js/sharing/loader.js',           # NEW
    ]
    
    for file in files_to_copy:
        src = static_src / file
        dst = static_dst / file
        if src.exists():
            shutil.copy2(src, dst)
            print(f"✓ Copied {file}")
```

**Action for Claude Code:**
- Modify `scripts/build.py`
- Add copying of sharing JS files

---

### Phase 7: Testing (2 hours)

**File**: `tests/test_sharing.py` (new)

```python
"""Test code sharing functionality"""
import pytest
from playwright.sync_api import Page, expect

def test_encoder_roundtrip():
    """Test encoding and decoding preserves code"""
    original_code = """can = Canvas(800, 600)
can.circle(400, 300, 100, fill=Color.RED)
can"""
    
    # Test will run in browser context
    # JS: encoded = await CodeEncoder.encode(original_code)
    # JS: decoded = await CodeEncoder.decode(encoded)
    # Assert: decoded === original_code
    pass

def test_share_button_generates_url(page: Page):
    """Test share button generates valid URL"""
    page.goto('http://localhost:8443/lessons/01-first-flower.html')
    
    # Click share button
    page.click('button:has-text("Share")')
    
    # Wait for modal
    expect(page.locator('.share-modal')).to_be_visible()
    
    # Check URL is generated
    share_input = page.locator('.share-url-input')
    expect(share_input).to_have_value(lambda v: v.startswith('http'))

def test_share_url_length_check(page: Page):
    """Test that oversized code shows error"""
    page.goto('http://localhost:8443/lessons/01-first-flower.html')
    
    # Fill editor with large code
    large_code = "can = Canvas(800, 600)\n" + "\n".join([
        f"can.circle({i}, {i}, 10, fill=Color.RED)"
        for i in range(1000)
    ])
    
    page.evaluate(f"window.editor.dispatch({{changes: {{from: 0, to: window.editor.state.doc.length, insert: {large_code!r}}}}})")
    
    # Click share
    page.click('button:has-text("Share")')
    
    # Should show error
    expect(page.locator('.share-error')).to_be_visible()
    expect(page.locator('.error-message')).to_contain_text('too long')

def test_load_shared_code(page: Page):
    """Test loading code from URL hash"""
    # Pre-encoded simple code
    encoded = "H4sIAAAAAAAAE6tWKkktLlGyUlAqSCxKVLJSUErLL1IqKMovL8nMSy_WUSrJSFWyMjQwAAKlWgA7XqBaJgAAAA=="
    
    page.goto(f'http://localhost:8443/lessons/01-first-flower.html#{encoded}')
    
    # Should show confirmation modal
    expect(page.locator('.shared-code-modal')).to_be_visible()
    
    # Click accept
    page.click('button:has-text("Load & Run")')
    
    # Code should be in editor
    # Canvas should render

def test_shared_code_security_validation(page: Page):
    """Test that malicious shared code is blocked"""
    # Encode code with forbidden import
    malicious_code = "import js\njs.document"
    # ... encode it ...
    
    page.goto(f'http://localhost:8443/lessons/01-first-flower.html#encoded')
    
    # Should show security warnings
    expect(page.locator('.security-warnings')).to_be_visible()
    expect(page.locator('.warning-note')).to_contain_text("won't run")

def test_copy_to_clipboard(page: Page):
    """Test copy button works"""
    page.goto('http://localhost:8443/lessons/01-first-flower.html')
    
    # Generate share link
    page.click('button:has-text("Share")')
    expect(page.locator('.share-modal')).to_be_visible()
    
    # Click copy
    page.click('.copy-btn')
    
    # Should show "Copied!"
    expect(page.locator('.copy-btn')).to_contain_text('Copied')
    
    # Clipboard should contain URL (needs clipboard permissions in test)
```

**Action for Claude Code:**
- Create `tests/test_sharing.py`
- Add Playwright tests for sharing flow
- Test encoding, UI, and security integration

---

## URL Structure

**Format:**
```
https://yoursite.com/lessons/[lesson-id].html#[encoded-code]
```

**Examples:**
```
Simple drawing (100 chars):
https://yoursite.com/lessons/01-first-flower.html#H4sIAAAAAAAAE6tW...

Complex drawing (1000 chars):
https://yoursite.com/lessons/15-final-project.html#H4sIAAAAAAAAE8VU...
```

**Encoding Details:**
- Original: ~100 chars Python code
- Gzip: ~60 bytes (40% reduction)
- Base64: ~80 chars (33% overhead)
- Total URL: ~120 chars (fits easily in 2000 limit)

---

## Security Integration

### Pre-Run Validation

Shared code goes through ALL security layers:

```
1. Load from hash
   ↓
2. Client-side validation (validator.js)
   ↓
3. Show confirmation to user
   ↓
4. User accepts
   ↓
5. Load into editor
   ↓
6. User clicks Run (or auto-run)
   ↓
7. Security validation (pre-execution)
   ↓
8. Worker execution (timeout + import whitelist)
   ↓
9. Canvas rendering
```

### User Warnings

**Confirmation modal shows:**
- "This is shared code from another user"
- Code preview (first 300 chars)
- Line count and character count
- Security validation results
- Option to decline

**If security issues:**
- Red warning banner
- List of specific issues
- "View Code Only" button (won't auto-run)
- Clear explanation of why it won't run

---

## User Experience Flow

### Creating a Share Link

```
1. Student writes code
2. Clicks "Share" button
3. Modal appears with link
4. Clicks "Copy" button
5. Link copied to clipboard
6. Shares link via chat/email/etc.
```

**What students see:**
```
┌─────────────────────────────────┐
│    📤 Share Your Drawing        │
├─────────────────────────────────┤
│ Copy this link to share:        │
│                                 │
│ [https://...#H4sI...]  [Copy]  │
│                                 │
│ Sharing Tips:                   │
│ • Works on any device           │
│ • No account needed             │
│ • Code is in the link           │
└─────────────────────────────────┘
```

### Viewing a Shared Link

```
1. Click link from classmate
2. Page loads with hash parameter
3. Confirmation modal appears
4. Preview code + security check
5. Click "Load & Run" or "Cancel"
6. Code loads + runs (if safe)
```

**What recipients see:**
```
┌─────────────────────────────────┐
│    ⚠️ Shared Code               │
├─────────────────────────────────┤
│ You're about to run code from   │
│ another user.                   │
│                                 │
│ Code Preview:                   │
│ can = Canvas(800, 600)          │
│ can.circle(400, 300, ...)       │
│                                 │
│ 📊 3 lines, 85 characters       │
│                                 │
│ [Cancel]  [Load & Run]          │
└─────────────────────────────────┘
```

---

## Edge Cases & Error Handling

### 1. Code Too Long

```javascript
if (urlLength > 2000) {
    showError(
        "Code too long for URL sharing!\n\n" +
        "Try:\n" +
        "• Remove comments\n" +
        "• Use shorter variable names\n" +
        "• Simplify the drawing"
    );
}
```

### 2. Corrupted URL

```javascript
try {
    code = await decode(hash);
} catch (error) {
    showError(
        "Failed to load shared code.\n" +
        "The link may be corrupted."
    );
}
```

### 3. Security Violations

```javascript
if (!validation.valid) {
    showWarning(
        "Security Issues:\n" +
        validation.errors.join('\n') +
        "\n\nCode will load but won't run."
    );
}
```

### 4. Browser Compatibility

```javascript
if (!window.CompressionStream) {
    showError(
        "Your browser doesn't support code sharing.\n" +
        "Please use Chrome, Edge, or Safari."
    );
}
```

---

## File Structure Summary

```
static/
├── js/
│   ├── sharing/
│   │   ├── encoder.js           # NEW: Compression + encoding
│   │   ├── share-manager.js     # NEW: Share UI logic
│   │   └── loader.js             # NEW: Load shared code
│   ├── security/
│   │   └── (existing security files)
│   └── app.js                    # MODIFY: Import sharing
│
templates/
├── components/
│   └── share-modal.html          # NEW: Share UI components
└── lesson.html.jinja             # MODIFY: Add share button

tests/
└── test_sharing.py               # NEW: Sharing tests

scripts/
└── build.py                      # MODIFY: Copy sharing files
```

---

## Implementation Timeline

| Phase | Task | Time |
|-------|------|------|
| 1 | Encoder/decoder | 2h |
| 2 | Share UI manager | 2h |
| 3 | Shared code loader | 2h |
| 4 | UI templates | 1h |
| 5 | App integration | 1h |
| 6 | Build updates | 30m |
| 7 | Testing | 2h |
| **Total** | | **10.5 hours** |

---

## Success Criteria

✅ Feature complete when:

1. **Share button generates valid URLs**
   - Compresses and encodes code
   - Checks length limits
   - Copies to clipboard

2. **Shared links load correctly**
   - Decodes without errors
   - Shows confirmation modal
   - Loads into editor

3. **Security integration works**
   - Shared code goes through validator
   - Shows security warnings if needed
   - Respects timeout and whitelist

4. **All tests pass**
   - Encoding round-trip
   - UI interactions
   - Security validation
   - Edge cases

5. **User experience is smooth**
   - Clear error messages
   - Responsive UI
   - Works on mobile
   - No confusing states

---

## Future Enhancements

After MVP is working:

1. **Server-side storage** (for longer code)
   - POST /api/share → {id: "abc123"}
   - GET /draw/abc123
   - Database: id, code, created_at

2. **QR codes** (for mobile sharing)
   - Generate QR from share URL
   - Display in modal
   - Scan to open on phone

3. **Gallery/showcase**
   - Public gallery of shared drawings
   - Upvote/like system
   - Featured drawings

4. **Remix/fork**
   - "Remix this drawing" button
   - Track derivations
   - Attribution

5. **Embed mode**
   - Iframe-friendly version
   - Read-only or interactive
   - For blogs/documentation

---

## Notes for Claude Code

**Dependencies:**
- Requires CompressionStream API (Chrome 80+, Safari 16.4+)
- No polyfill needed (graceful degradation)

**Testing:**
- Test with lesson starter code (should always fit)
- Test with max-length code (~1500 chars)
- Test malicious code patterns
- Test on mobile browsers

**Security:**
- Shared code MUST go through same validation as typed code
- NO bypass of security layers
- User MUST confirm before running
- Show clear warnings

**UX:**
- Keep it simple - one button, one modal
- Clear error messages
- Mobile-friendly
- Keyboard accessible

---

**Prerequisites:** Security implementation complete (from SECURITY_IMPLEMENTATION_PLAN.md)

**Ready for implementation after security Phase 8 is complete.**