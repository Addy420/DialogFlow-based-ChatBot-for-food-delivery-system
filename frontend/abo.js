document.addEventListener("DOMContentLoaded", function() {
    const slideshowContainer = document.querySelector(".slideshow-container");
    const slides = document.querySelectorAll(".slideshow-slide");
    const prevButton = document.querySelector(".slideshow-prev");
    const nextButton = document.querySelector(".slideshow-next");

    let currentSlide = 0;

    function showSlide(index) {
        slideshowContainer.style.transform = `translateX(-${index * 100}%)`;
        currentSlide = index;
    }

    // Navigate to the next slide
    nextButton.addEventListener("click", function() {
        const newSlide = (currentSlide + 1) % slides.length;
        showSlide(newSlide);
    });

    // Navigate to the previous slide
    prevButton.addEventListener("click", function() {
        const newSlide = (currentSlide - 1 + slides.length) % slides.length;
        showSlide(newSlide);
    });

    // Auto-slide every 5 seconds
    setInterval(() => {
        const newSlide = (currentSlide + 1) % slides.length;
        showSlide(newSlide);
    }, 5000); // Auto-slide interval

    // Scroll to specific section
    window.scrollToSection = function(sectionId) {
        const targetElement = document.querySelector(sectionId);
        if (targetElement) {
            targetElement.scrollIntoView({ behavior: "smooth" });
        }
    };
});