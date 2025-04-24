// ✅ Select all animated elements
const animatedElements = document.querySelectorAll('.animate-on-scroll');

// ✅ Intersection Observer Setup
const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('show');
        } else {
            entry.target.classList.remove('show'); // ✅ Reset animation on scroll
        }
    });
}, {
    threshold: 0.2, // Trigger when 20% of element is visible
});

// ✅ Observe each element
animatedElements.forEach(element => {
    observer.observe(element);
});

// ✅ Smooth Scroll to Real-Time Cases Section
function scrollToCases(event) {
    event.preventDefault(); // ✅ Prevent default anchor behavior
    const pageHeight = document.documentElement.scrollHeight;
    const offsetTop = window.scrollY; // 200px above current scroll position


    // ✅ Smooth Scroll to Target Section
    window.scrollTo({
        top: offsetTop,
        behavior: 'smooth'
    });
}

// ✅ Toggle Sidebar and Menu Icon
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuIcon = document.getElementById('menuIcon');
    
    sidebar.classList.toggle('open');
    menuIcon.classList.toggle('open');

    // ✅ Inline Style to Force Color Change
    if (menuIcon.classList.contains('open')) {
        menuIcon.style.color = '#fff'; // White when open
    } else {
        menuIcon.style.color = '#000'; // Black when closed
    }
}
