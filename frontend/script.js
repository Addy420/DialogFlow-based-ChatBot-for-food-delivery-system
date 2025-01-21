// script.js

document.addEventListener("DOMContentLoaded", function() {
    const orderButton = document.querySelector(".order-now");
    const chatbotPopup = document.querySelector(".chatbot-popup");
    const closePopup = document.querySelector(".close-popup");
    const navLinks = document.querySelectorAll(".menu ul li a");

    orderButton.addEventListener("click", function() {
        chatbotPopup.style.display = "block";
    });

    closePopup.addEventListener("click", function() {
        chatbotPopup.style.display = "none";
    });

    // Smooth scrolling for navigation links
    navLinks.forEach(link => {
        link.addEventListener("click", function(event) {
            event.preventDefault();
            const targetId = this.getAttribute("href").substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                const offsetTop = targetElement.offsetTop;
                window.scrollTo({
                    top: offsetTop,
                    behavior: "smooth"
                });
            }
        });
    });
});

