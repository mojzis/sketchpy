import { SecurityConfig } from './config.dev.js';

/**
 * Manages code execution in isolated Web Worker with timeout
 * Each execution gets a fresh worker if previous timed out
 */
export class CodeExecutor {
    constructor() {
        this.worker = null;
        this.pendingExecutions = new Map();
        this.executionId = 0;
        this.isWorkerReady = false;

        this.initWorker();
    }

    /**
     * Initialize or reinitialize worker
     */
    initWorker() {
        // Clean up old worker if exists
        if (this.worker) {
            this.worker.terminate();
        }

        // Determine worker path based on current page location (for file:// compatibility)
        const isInLessonsDir = window.location.pathname.includes('/lessons/');
        const workerPath = isInLessonsDir
            ? '../static/js/pyodide-worker.js'
            : 'static/js/pyodide-worker.js';

        this.worker = new Worker(workerPath);
        this.isWorkerReady = false;

        // Handle worker messages
        this.worker.onmessage = (event) => {
            const { id, type, success, data, error } = event.data;

            if (type === 'ready') {
                this.isWorkerReady = true;
                console.log('✓ Pyodide worker ready');
                return;
            }

            if (type === 'result') {
                const pending = this.pendingExecutions.get(id);

                if (pending) {
                    clearTimeout(pending.timeout);

                    if (success) {
                        pending.resolve(data);
                    } else {
                        pending.reject(new Error(error));
                    }

                    this.pendingExecutions.delete(id);
                }
            }
        };

        // Handle worker errors
        this.worker.onerror = (error) => {
            console.error('Worker error:', error);
            // Reject all pending executions
            for (const [execId, pending] of this.pendingExecutions) {
                clearTimeout(pending.timeout);
                pending.reject(new Error('Worker crashed: ' + error.message));
            }
            this.pendingExecutions.clear();

            // Reinitialize worker
            this.initWorker();
        };
    }

    /**
     * Execute Python code with timeout protection
     * @param {string} code - Python code to execute
     * @param {number} timeoutMs - Timeout in milliseconds (default from config)
     * @returns {Promise<string>} SVG output from canvas
     */
    async execute(code, timeoutMs = SecurityConfig.TIMEOUT_MS) {
        // Wait for worker to be ready
        if (!this.isWorkerReady) {
            await this.waitForReady();
        }

        return new Promise((resolve, reject) => {
            const id = this.executionId++;

            // Create timeout that terminates worker
            const timeout = setTimeout(() => {
                this.pendingExecutions.delete(id);

                // Kill the worker (it's frozen)
                this.worker.terminate();

                // Create new worker for next execution
                this.initWorker();

                reject(new Error(
                    `⏱️ Execution timeout (${timeoutMs / 1000}s limit)\n\n` +
                    'Your code took too long to run. Possible causes:\n' +
                    '• Infinite loop (while True, etc.)\n' +
                    '• Too many shapes (try fewer iterations)\n' +
                    '• Complex calculations'
                ));
            }, timeoutMs);

            // Store pending execution
            this.pendingExecutions.set(id, {
                resolve,
                reject,
                timeout,
                startTime: Date.now()
            });

            // Send to worker
            this.worker.postMessage({
                id,
                type: 'execute',
                code
            });
        });
    }

    /**
     * Wait for worker to initialize
     */
    async waitForReady(maxWaitMs = 30000) {
        const startTime = Date.now();

        while (!this.isWorkerReady) {
            if (Date.now() - startTime > maxWaitMs) {
                throw new Error('Worker initialization timeout');
            }
            await new Promise(resolve => setTimeout(resolve, 100));
        }
    }

    /**
     * Terminate worker and clean up
     */
    destroy() {
        if (this.worker) {
            this.worker.terminate();
            this.worker = null;
        }

        // Reject all pending
        for (const [_execId, pending] of this.pendingExecutions) {
            clearTimeout(pending.timeout);
            pending.reject(new Error('Executor destroyed'));
        }
        this.pendingExecutions.clear();
    }
}

// Global singleton instance
export const executor = new CodeExecutor();
