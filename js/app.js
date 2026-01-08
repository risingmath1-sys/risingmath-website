document.addEventListener('DOMContentLoaded', () => {
    // Scroll Animations
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.1
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                // Optional: Stop observing once animations run
                // observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const animatedElements = document.querySelectorAll('.fade-in, .fade-up');
    animatedElements.forEach(el => observer.observe(el));

    // Header Scroll Effect
    const header = document.querySelector('header');
    if (header) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 50) {
                header.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
                if (window.innerWidth > 768) {
                    header.style.height = '70px';
                }
            } else {
                header.style.boxShadow = 'none';
                if (window.innerWidth > 768) {
                    header.style.height = '80px';
                }
            }
        });
    }

    // Carousel Logic
    let slideIndex = 1;
    const slides = document.getElementsByClassName("carousel-slide");

    // Only run carousel logic if slides exist
    if (slides.length > 0) {
        showSlides(slideIndex);

        const prevBtn = document.querySelector('.prev-btn');
        const nextBtn = document.querySelector('.next-btn');
        const dots = document.querySelectorAll('.dot');

        if (prevBtn && nextBtn) {
            prevBtn.addEventListener('click', () => plusSlides(-1));
            nextBtn.addEventListener('click', () => plusSlides(1));
        }

        if (dots) {
            dots.forEach((dot, index) => {
                dot.addEventListener('click', () => currentSlide(index + 1));
            });
        }

        // Auto Slide
        setInterval(() => {
            plusSlides(1);
        }, 3500); // Change image every 3.5 seconds
    }

    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    function currentSlide(n) {
        showSlides(slideIndex = n);
    }

    function showSlides(n) {
        let i;
        let slides = document.getElementsByClassName("carousel-slide");
        let dots = document.getElementsByClassName("dot");

        if (slides.length === 0) return;

        if (n > slides.length) { slideIndex = 1 }
        if (n < 1) { slideIndex = slides.length }

        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
            slides[i].classList.remove("active");
        }

        if (dots.length > 0) {
            for (i = 0; i < dots.length; i++) {
                dots[i].classList.remove("active");
            }
            dots[slideIndex - 1].classList.add("active");
        }

        slides[slideIndex - 1].style.display = "flex";
        slides[slideIndex - 1].classList.add("active");
    }

    // 4. Sticky Side Menu Haptic Feedback
    const stickyTabs = document.querySelectorAll('.sticky-tab');
    stickyTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            if (navigator.vibrate) {
                navigator.vibrate(10);
            }
        });
    });


    // --- Gallery Lightbox Logic ---

    // 1. Ensure Lightbox Exists (Inject if missing)
    let lightbox = document.getElementById('lightbox');
    let lightboxImg = document.getElementById('lightbox-img');
    let closeBtn = document.querySelector('.lightbox-close');

    if (!lightbox) {
        // Create Lightbox HTML Structure
        lightbox = document.createElement('div');
        lightbox.id = 'lightbox';
        lightbox.className = 'lightbox-modal';

        closeBtn = document.createElement('span');
        closeBtn.className = 'lightbox-close';
        closeBtn.innerHTML = '&times;';

        lightboxImg = document.createElement('img');
        lightboxImg.className = 'lightbox-content';
        lightboxImg.id = 'lightbox-img';

        lightbox.appendChild(closeBtn);
        lightbox.appendChild(lightboxImg);
        document.body.appendChild(lightbox);
    }

    // 2. Setup Lightbox Close Events
    const closeLightbox = () => {
        lightbox.style.display = 'none';
        lightboxImg.src = ''; // Clear source
    };

    if (closeBtn) {
        closeBtn.addEventListener('click', closeLightbox);
    }

    if (lightbox) {
        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                closeLightbox();
            }
        });
    }

    // 3. Gallery Item Clicks (only if gallery exists)
    const galleryItems = document.querySelectorAll('.gallery-item');
    if (galleryItems.length > 0) {
        galleryItems.forEach(item => {
            item.addEventListener('click', () => {
                const img = item.querySelector('img');
                if (img && lightbox && lightboxImg) {
                    lightbox.style.display = 'flex';
                    lightboxImg.src = img.src;
                }
            });
        });
    }

    // --- Notice Link Override (Price Image Popup) ---
    // Target all links pointing to notice.html (flexible match)
    const noticeLinks = document.querySelectorAll('a[href*="notice.html"]');
    const priceImgPath = './images/academy/200_price.webp';

    console.log(`[App.js] Found ${noticeLinks.length} notice links.`);

    noticeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Prevent Navigation
            console.log('[App.js] Notice link clicked.');

            if (lightbox && lightboxImg) {
                // Force styles ensuring visibility
                lightbox.style.display = 'flex';
                lightbox.style.zIndex = '99999'; // Force High Z-Index
                lightbox.style.position = 'fixed';
                lightbox.style.top = '0';
                lightbox.style.left = '0';
                lightbox.style.width = '100%';
                lightbox.style.height = '100%';
                lightbox.style.backgroundColor = 'rgba(255, 255, 255, 0.98)';

                lightboxImg.src = priceImgPath;
                console.log(`[App.js] Lightbox opened with: ${priceImgPath}`);
            } else {
                console.error('[App.js] Lightbox elements missing!');
            }
        });
    });
    // --- Mobile Circular Menu Logic ---
    const mobileMenuTrigger = document.getElementById('mobileMenuTrigger');
    const circularMenuItems = document.getElementById('circularMenuItems');

    if (mobileMenuTrigger && circularMenuItems) {
        mobileMenuTrigger.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent document click from closing immediately
            circularMenuItems.classList.toggle('active');

            // Optional: Animate icon
            const icon = mobileMenuTrigger.querySelector('i');
            if (icon) {
                if (circularMenuItems.classList.contains('active')) {
                    icon.classList.remove('ri-menu-line');
                    icon.classList.add('ri-close-line');
                } else {
                    icon.classList.remove('ri-close-line');
                    icon.classList.add('ri-menu-line');
                }
            }
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (circularMenuItems.classList.contains('active')) {
                // If click is not inside the menu container
                if (!mobileMenuTrigger.contains(e.target) && !circularMenuItems.contains(e.target)) {
                    circularMenuItems.classList.remove('active');

                    // Reset icon
                    const icon = mobileMenuTrigger.querySelector('i');
                    if (icon) {
                        icon.classList.remove('ri-close-line');
                        icon.classList.add('ri-menu-line');
                    }
                }
            }
        });
    }
});
