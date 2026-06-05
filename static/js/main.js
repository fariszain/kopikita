// KopiKita - Premium & Interactive JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // 1. Ambience Ambient Orbs (dynamically insert if not present)
    if (!document.querySelector('.bg-ambient')) {
        const ambientContainer = document.createElement('div');
        ambientContainer.className = 'bg-ambient';
        
        const orb1 = document.createElement('div');
        orb1.className = 'bg-orb bg-orb-1';
        
        const orb2 = document.createElement('div');
        orb2.className = 'bg-orb bg-orb-2';
        
        ambientContainer.appendChild(orb1);
        ambientContainer.appendChild(orb2);
        document.body.appendChild(ambientContainer);
    }

    // 2. Custom Cursor Glow following mouse movement
    const cursorGlow = document.createElement('div');
    cursorGlow.className = 'cursor-glow';
    document.body.appendChild(cursorGlow);

    document.addEventListener('mousemove', (e) => {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });

    // 3. Navbar scroll effect
    const navbar = document.getElementById('navbar');
    if (navbar) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // 4. Mobile Navigation Toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.getElementById('navLinks');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', () => {
            navLinks.classList.toggle('open');
            navToggle.classList.toggle('active');
        });

        document.addEventListener('click', (e) => {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('open');
                navToggle.classList.remove('active');
            }
        });
    }

    // 5. Interactive Card Parallax Tilt Effect on Hover
    const interactiveCards = document.querySelectorAll('.menu-card, .category-card, .why-card, .value-card, .team-card');
    interactiveCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left; // x position within the element
            const y = e.clientY - rect.top;  // y position within the element
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calculate tilt degrees (max 6 degrees)
            const tiltX = ((y - centerY) / centerY) * -6;
            const tiltY = ((x - centerX) / centerX) * 6;
            
            card.style.transform = `perspective(1000px) rotateX(${tiltX}deg) rotateY(${tiltY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0)';
        });
    });

    // 6. Smooth Fade-In and Entrance Animations with Intersection Observer
    const animateOnScroll = () => {
        const observerOptions = {
            threshold: 0.05,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-view');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        interactiveCards.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'opacity 0.8s cubic-bezier(0.16, 1, 0.3, 1), transform 0.8s cubic-bezier(0.16, 1, 0.3, 1)';
            observer.observe(el);
            
            // Dynamically define a class for in-view
            el.addEventListener('transitionend', function handler() {
                if (el.classList.contains('in-view')) {
                    // Reset transform transition to allow custom hover tilt
                    el.style.transition = 'transform 0.2s ease-out, border-color 0.4s ease, box-shadow 0.4s ease';
                    el.removeEventListener('transitionend', handler);
                }
            });
        });

        // Insert in-view styles dynamically
        const styleSheet = document.createElement("style");
        styleSheet.innerText = `
            .in-view {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(styleSheet);
    };

    animateOnScroll();

    // 7. Auto-dismiss flash messages
    setTimeout(() => {
        document.querySelectorAll('.flash-msg').forEach(msg => {
            msg.style.transition = 'all 0.5s cubic-bezier(0.16, 1, 0.3, 1)';
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(120%)';
            setTimeout(() => msg.remove(), 500);
        });
    }, 5000);
});
