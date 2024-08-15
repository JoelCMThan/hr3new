// Custom JavaScript

// Example: Toggle visibility of a password field
function togglePasswordVisibility() {
    const passwordField = document.getElementById('password');
    const toggleButton = document.getElementById('togglePassword');
    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleButton.innerText = 'Hide';
    } else {
        passwordField.type = 'password';
        toggleButton.innerText = 'Show';
    }
}

// Attach event listeners when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', function () {
    const toggleButton = document.getElementById('togglePassword');
    if (toggleButton) {
        toggleButton.addEventListener('click', togglePasswordVisibility);
    }
});
