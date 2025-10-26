/**
 * Alpine.js app state for sketchpy learning platform
 */

function appState() {
    return {
        // Execution state
        isRunning: false,

        // Current lesson
        lesson: window.CURRENT_LESSON || null,

        // Initialization
        init() {
            console.log('Alpine initialized');
            console.log('Current lesson:', this.lesson?.id);
        }
    }
}

// Make globally available
window.appState = appState;
