window.addEventListener('DOMContentLoaded', (event) => {
    console.log('Website loaded');

    // Accessibility: Ensure the first headline is focusable on load
    const firstHeadline = document.querySelector('h1');
    firstHeadline.setAttribute('tabindex', '0');
    firstHeadline.focus();

    // Additional accessibility improvements
    let sectionLinks = document.querySelectorAll('section h2');
    sectionLinks.forEach(section => {
        section.setAttribute('role', 'heading');
        section.setAttribute('aria-level', '2');
    });

    // Improved responsive design for images and text
    const images = document.querySelectorAll('img');
    images.forEach(image => {
        image.setAttribute('loading', 'lazy'); // Lazy load images
    });

    // Adding button functionality for enhanced interactivity
    const button = document.querySelector('.view-more-btn');
    button.onclick = function() {
        alert('More memories coming soon!');
    };
});