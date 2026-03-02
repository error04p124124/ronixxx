/**
 * Modern Glassmorphism Inventory System
 * Advanced JavaScript with smooth animations
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all features
    initAnimations();
    initNavbar();
    initCards();
    initForms();
    initTables();
    initAlerts();
    initCounters();
    initBootstrap();
    initParticles();
    
    console.log('✨ Modern Glassmorphism System Initialized');
});

/**
 * Initialize scroll animations
 */
function initAnimations() {
    const animatedElements = document.querySelectorAll('.card, .page-header, .alert');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in-up');
                    entry.target.style.opacity = '1';
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(element => {
        element.style.opacity = '0';
        observer.observe(element);
    });
}

/**
 * Enhanced navbar with scroll effects
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    if (!navbar) return;
    
    let lastScroll = 0;
    let ticking = false;
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => {
                const currentScroll = window.pageYOffset;
                
                if (currentScroll > 100) {
                    navbar.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.6)';
                    navbar.style.backdropFilter = 'blur(30px)';
                } else {
                    navbar.style.boxShadow = '0 4px 16px rgba(0, 0, 0, 0.4)';
                    navbar.style.backdropFilter = 'blur(20px)';
                }
                
                lastScroll = currentScroll;
                ticking = false;
            });
            
            ticking = true;
        }
    });
    
    // Active link highlighting
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

/**
 * Enhanced card interactions
 */
function initCards() {
    const cards = document.querySelectorAll('.card');
    
    cards.forEach(card => {
        // Click ripple effect
        card.addEventListener('click', function(e) {
            const ripple = document.createElement('div');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.style.position = 'absolute';
            ripple.style.borderRadius = '50%';
            ripple.style.background = 'rgba(255, 255, 255, 0.3)';
            ripple.style.pointerEvents = 'none';
            ripple.style.animation = 'ripple 0.8s ease-out';
            
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            
            setTimeout(() => ripple.remove(), 800);
        });
    });
    
    // Add ripple animation
    if (!document.getElementById('ripple-animation')) {
        const style = document.createElement('style');
        style.id = 'ripple-animation';
        style.textContent = `
            @keyframes ripple {
                from {
                    transform: scale(0);
                    opacity: 1;
                }
                to {
                    transform: scale(2);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Form enhancements
 */
function initForms() {
    // Real-time validation
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
        
        // Add floating labels effect
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            // Focus effect
            input.addEventListener('focus', function() {
                this.style.transform = 'scale(1.02)';
                this.style.boxShadow = '0 0 20px rgba(79, 172, 254, 0.3)';
            });
            
            input.addEventListener('blur', function() {
                this.style.transform = '';
                this.style.boxShadow = '';
                
                // Validation feedback
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else if (this.value) {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

/**
 * Table enhancements
 */
function initTables() {
    // Search functionality
    const searchInputs = document.querySelectorAll('[data-table-search]');
    
    searchInputs.forEach(input => {
        const tableId = input.dataset.tableSearch;
        const table = document.getElementById(tableId);
        
        if (!table) return;
        
        input.addEventListener('input', debounce(function() {
            const searchTerm = this.value.toLowerCase();
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                const shouldShow = text.includes(searchTerm);
                
                row.style.transition = 'all 0.3s ease';
                
                if (shouldShow) {
                    row.style.display = '';
                    row.style.opacity = '1';
                    row.style.transform = 'scale(1)';
                } else {
                    row.style.opacity = '0';
                    row.style.transform = 'scale(0.95)';
                    setTimeout(() => {
                        if (row.style.opacity === '0') {
                            row.style.display = 'none';
                        }
                    }, 300);
                }
            });
        }, 300));
    });
    
    // Row hover effects
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 4px 16px rgba(79, 172, 254, 0.2)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
}

/**
 * Enhanced alerts with auto-hide
 */
function initAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach((alert, index) => {
        // Stagger animation
        setTimeout(() => {
            alert.style.animation = 'fadeInUp 0.5s ease-out forwards';
        }, index * 100);
        
        // Add progress bar
        const progressBar = document.createElement('div');
        progressBar.style.cssText = `
            position: absolute;
            bottom: 0;
            left: 0;
            height: 3px;
            background: currentColor;
            width: 100%;
            opacity: 0.5;
            animation: shrink 5s linear forwards;
        `;
        alert.style.position = 'relative';
        alert.appendChild(progressBar);
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            alert.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
    
    // Add shrink animation
    if (!document.getElementById('shrink-animation')) {
        const style = document.createElement('style');
        style.id = 'shrink-animation';
        style.textContent = `
            @keyframes shrink {
                from { width: 100%; }
                to { width: 0%; }
            }
            @keyframes fadeOut {
                from {
                    opacity: 1;
                    transform: translateY(0);
                }
                to {
                    opacity: 0;
                    transform: translateY(-20px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Close button functionality
    document.querySelectorAll('.alert .btn-close').forEach(button => {
        button.addEventListener('click', function() {
            const alert = this.closest('.alert');
            alert.style.animation = 'fadeOut 0.5s ease-out forwards';
            setTimeout(() => alert.remove(), 500);
        });
    });
}

/**
 * Animated counters for stat cards
 */
function initCounters() {
    const counters = document.querySelectorAll('.stat-value');
    
    const observerOptions = {
        threshold: 0.5
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                animateCounter(entry.target);
            }
        });
    }, observerOptions);
    
    counters.forEach(counter => observer.observe(counter));
}

/**
 * Animate counter to target value
 */
function animateCounter(element) {
    const text = element.textContent;
    const number = parseFloat(text.replace(/[^\d.-]/g, ''));
    
    if (isNaN(number)) return;
    
    const duration = 2000;
    const steps = 60;
    const increment = number / steps;
    const stepDuration = duration / steps;
    
    let current = 0;
    let step = 0;
    
    const timer = setInterval(() => {
        step++;
        current += increment;
        
        if (step >= steps) {
            element.textContent = formatNumber(number);
            clearInterval(timer);
        } else {
            element.textContent = formatNumber(current);
        }
    }, stepDuration);
}

/**
 * Format number for display
 */
function formatNumber(num) {
    if (num % 1 === 0) {
        return Math.round(num).toLocaleString('ru-RU');
    }
    return num.toFixed(2).toLocaleString('ru-RU');
}

/**
 * Initialize Bootstrap components
 */
function initBootstrap() {
    // Tooltips
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl, {
            template: '<div class="tooltip glass" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>'
        });
    });
    
    // Popovers
    const popoverTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="popover"]')
    );
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Background particles effect (subtle)
 */
function initParticles() {
    const canvas = document.createElement('canvas');
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        opacity: 0.7;
    `;
    document.body.appendChild(canvas);
    
    const ctx = canvas.getContext('2d');
    let particles = [];
    
    function resize() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resize();
    window.addEventListener('resize', resize);
    
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 3 + 1.5;
            this.speedX = Math.random() * 0.5 - 0.25;
            this.speedY = Math.random() * 0.5 - 0.25;
            this.color = `rgba(${30 + Math.random() * 60}, ${30 + Math.random() * 60}, ${30 + Math.random() * 60}, ${Math.random() * 0.5 + 0.3})`;
        }
        
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            if (this.x > canvas.width) this.x = 0;
            if (this.x < 0) this.x = canvas.width;
            if (this.y > canvas.height) this.y = 0;
            if (this.y < 0) this.y = canvas.height;
        }
        
        draw() {
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    function init() {
        particles = [];
        const particleCount = Math.floor((canvas.width * canvas.height) / 15000);
        for (let i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }
    }
    
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        particles.forEach(particle => {
            particle.update();
            particle.draw();
        });
        
        requestAnimationFrame(animate);
    }
    
    init();
    animate();
}

/**
 * Utility: Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Utility: Show notification
 */
function showNotification(message, type = 'info', duration = 5000) {
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        animation: fadeInUp 0.5s ease-out;
    `;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alert);
    
    setTimeout(() => {
        alert.style.animation = 'fadeOut 0.5s ease-out forwards';
        setTimeout(() => alert.remove(), 500);
    }, duration);
}

/**
 * Utility: Confirm dialog
 */
function confirmDelete(message = 'Вы уверены, что хотите удалить этот элемент?') {
    return confirm(message);
}

/**
 * Utility: Loading state
 */
function showLoading(button) {
    const originalText = button.innerHTML;
    button.dataset.originalText = originalText;
    button.disabled = true;
    button.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2"></span>
        Загрузка...
    `;
}

function hideLoading(button) {
    if (button.dataset.originalText) {
        button.innerHTML = button.dataset.originalText;
        button.disabled = false;
        delete button.dataset.originalText;
    }
}

/**
 * Utility: Copy to clipboard
 */
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('✅ Скопировано в буфер обмена', 'success', 2000);
        }).catch(err => {
            console.error('Failed to copy:', err);
            showNotification('❌ Ошибка копирования', 'danger', 2000);
        });
    } else {
        // Fallback
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            showNotification('✅ Скопировано в буфер обмена', 'success', 2000);
        } catch (err) {
            console.error('Failed to copy:', err);
            showNotification('❌ Ошибка копирования', 'danger', 2000);
        }
        
        document.body.removeChild(textarea);
    }
}

/**
 * Utility: Format currency
 */
function formatCurrency(amount, currency = 'RUB') {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: currency
    }).format(amount);
}

/**
 * Utility: Format date
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Intl.DateTimeFormat('ru-RU', {
        ...defaultOptions,
        ...options
    }).format(new Date(date));
}

// Export utilities to global scope
window.inventorySystem = {
    showNotification,
    confirmDelete,
    showLoading,
    hideLoading,
    copyToClipboard,
    formatCurrency,
    formatDate,
    debounce
};
