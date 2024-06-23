const modeToggle = document.getElementById('mode-toggle');
const body = document.body;

modeToggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        modeToggle.textContent = 'Switch to Light Mode';
    } else {
        modeToggle.textContent = 'Switch to Dark Mode';
    }
});