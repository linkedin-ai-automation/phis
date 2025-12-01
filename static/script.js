// Session tracking
let sessionData = {
    sessionId: generateSessionId(),
    pageLoadTime: new Date(),
    activities: []
};

function generateSessionId() {
    return 'SESSION_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Log activity
async function logActivity(action, details = {}) {
    const activity = {
        action: action,
        timestamp: new Date().toISOString(),
        timeFromLoad: (new Date() - sessionData.pageLoadTime) / 1000,
        details: details,
        sessionId: sessionData.sessionId,
        userAgent: navigator.userAgent,
        screenResolution: `${screen.width}x${screen.height}`,
        language: navigator.language
    };
    
    sessionData.activities.push(activity);
    
    try {
        await fetch('/log-activity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(activity)
        });
    } catch (error) {
        console.error('Error logging activity:', error);
    }
}

window.addEventListener('load', () => {
    logActivity('page_loaded', { url: window.location.href });
});

function logActivityAndShowModal(action) {
    logActivity(action);
    
    // Direct redirect to venue map - skip login completely
    window.location.href = '/venue-map';
}

// Close on outside click (kept for compatibility but not used)
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
        logActivity('modal_closed_outside');
    }
}

// Track page unload
window.addEventListener('beforeunload', () => {
    logActivity('page_unload', {
        timeOnPage: (new Date() - sessionData.pageLoadTime) / 1000
    });
});
