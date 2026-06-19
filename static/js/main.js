// MindGuard Common JavaScript Utility

// Function to display the Emergency Helplines modal
function showEmergency() {
    const modalElement = document.getElementById('emergencyModal');
    if (modalElement) {
        // Initialize and show the Bootstrap modal
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    } else {
        // Fallback in case the modal element is not in the DOM
        alert("Immediate Support Helplines:\n\n- India: iCall (022-25521111) | AASRA (91-9820466726)\n- International: Find a local helpline at befrienders.org\n\nYou are not alone. Please reach out to someone who can help.");
    }
}