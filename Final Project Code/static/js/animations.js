// Register ScrollTrigger plugin
gsap.registerPlugin(ScrollTrigger);

// Initialize animations when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Animate navigation items
    gsap.from('nav a', {
        duration: 0.5,
        y: -20,
        opacity: 0,
        stagger: 0.1,
        ease: 'power2.out'
    });

    // Animate main content
    gsap.from('main > *', {
        scrollTrigger: {
            trigger: 'main',
            start: 'top 80%',
            toggleActions: 'play none none reverse'
        },
        duration: 0.8,
        y: 50,
        opacity: 0,
        stagger: 0.2,
        ease: 'power2.out'
    });

    // Animate footer
    gsap.from('footer', {
        scrollTrigger: {
            trigger: 'footer',
            start: 'top 90%',
            toggleActions: 'play none none reverse'
        },
        duration: 0.8,
        y: 50,
        opacity: 0,
        ease: 'power2.out'
    });

    // Animate cards and sections
    gsap.utils.toArray('.card, section').forEach(element => {
        gsap.from(element, {
            scrollTrigger: {
                trigger: element,
                start: 'top 80%',
                toggleActions: 'play none none reverse'
            },
            duration: 0.8,
            y: 50,
            opacity: 0,
            ease: 'power2.out'
        });
    });

    // Animate buttons
    gsap.from('button, .btn', {
        duration: 0.5,
        scale: 0.8,
        opacity: 0,
        stagger: 0.1,
        ease: 'back.out(1.7)'
    });

    // Animate form elements
    gsap.from('form input, form select, form textarea', {
        duration: 0.5,
        x: -20,
        opacity: 0,
        stagger: 0.1,
        ease: 'power2.out'
    });

    // Add hover animations to buttons
    document.querySelectorAll('button, .btn, a.btn').forEach(button => {
        button.addEventListener('mouseenter', () => {
            gsap.to(button, {
                scale: 1.05,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        button.addEventListener('mouseleave', () => {
            gsap.to(button, {
                scale: 1,
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });

    // Add hover animations to cards
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', () => {
            gsap.to(card, {
                y: -10,
                boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
        
        card.addEventListener('mouseleave', () => {
            gsap.to(card, {
                y: 0,
                boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
                duration: 0.3,
                ease: 'power2.out'
            });
        });
    });
}); 