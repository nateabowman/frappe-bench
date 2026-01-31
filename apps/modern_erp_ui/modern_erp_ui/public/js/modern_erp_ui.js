/**
 * Modern ERP UI - Enhanced JavaScript
 * Provides modern interactions, animations, and UX improvements
 */

class ModernERPUI {
    constructor() {
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        this.enhanceButtons();
        this.enhanceForms();
        this.enhanceTables();
        this.enhanceCards();
        this.setupSmoothScrolling();
        this.setupTooltips();
        this.setupAnimations();
        this.setupKeyboardShortcuts();
        this.observeThemeChanges();
    }

    /**
     * Enhance buttons with modern interactions
     */
    enhanceButtons() {
        const buttons = document.querySelectorAll('.btn');
        
        buttons.forEach(button => {
            // Add ripple effect
            button.addEventListener('click', (e) => {
                this.createRipple(e, button);
            });

            // Add loading state
            if (button.type === 'submit' || button.classList.contains('btn-primary')) {
                button.addEventListener('click', () => {
                    if (!button.disabled) {
                        this.setButtonLoading(button, true);
                    }
                });
            }
        });
    }

    /**
     * Create ripple effect on button click
     */
    createRipple(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;

        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');

        // Add ripple styles if not already present
        if (!document.getElementById('ripple-styles')) {
            const style = document.createElement('style');
            style.id = 'ripple-styles';
            style.textContent = `
                .btn {
                    position: relative;
                    overflow: hidden;
                }
                .ripple {
                    position: absolute;
                    border-radius: 50%;
                    background: rgba(255, 255, 255, 0.6);
                    transform: scale(0);
                    animation: ripple-animation 0.6s ease-out;
                    pointer-events: none;
                }
                @keyframes ripple-animation {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }

        element.appendChild(ripple);
        setTimeout(() => ripple.remove(), 600);
    }

    /**
     * Set button loading state
     */
    setButtonLoading(button, isLoading) {
        if (isLoading) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<span class="spinner"></span> Loading...';
            button.disabled = true;
        } else {
            button.innerHTML = button.dataset.originalText || button.innerHTML;
            button.disabled = false;
        }
    }

    /**
     * Enhance form inputs with floating labels and validation
     */
    enhanceForms() {
        const inputs = document.querySelectorAll('.form-control, .form-select');
        
        inputs.forEach(input => {
            // Add focus animations
            input.addEventListener('focus', () => {
                input.parentElement?.classList.add('focused');
            });

            input.addEventListener('blur', () => {
                input.parentElement?.classList.remove('focused');
                this.validateInput(input);
            });

            // Real-time validation
            input.addEventListener('input', () => {
                this.validateInput(input);
            });
        });
    }

    /**
     * Validate input and show feedback
     */
    validateInput(input) {
        const value = input.value.trim();
        const parent = input.parentElement;
        
        // Remove existing feedback
        parent.querySelector('.invalid-feedback')?.remove();
        input.classList.remove('is-invalid', 'is-valid');

        // Basic validation
        if (input.required && !value) {
            input.classList.add('is-invalid');
            this.showValidationError(input, 'This field is required');
        } else if (value && input.type === 'email' && !this.isValidEmail(value)) {
            input.classList.add('is-invalid');
            this.showValidationError(input, 'Please enter a valid email address');
        } else if (value) {
            input.classList.add('is-valid');
        }
    }

    /**
     * Show validation error message
     */
    showValidationError(input, message) {
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        feedback.style.display = 'block';
        input.parentElement.appendChild(feedback);
    }

    /**
     * Validate email format
     */
    isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    /**
     * Enhance tables with sorting and filtering
     */
    enhanceTables() {
        const tables = document.querySelectorAll('.table');
        
        tables.forEach(table => {
            // Add hover effects to rows
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(row => {
                row.addEventListener('mouseenter', () => {
                    row.style.transition = 'all 0.2s ease';
                });
            });

            // Make table responsive
            if (!table.parentElement.classList.contains('table-responsive')) {
                const wrapper = document.createElement('div');
                wrapper.className = 'table-responsive';
                table.parentElement.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            }
        });
    }

    /**
     * Enhance cards with hover effects
     */
    enhanceCards() {
        const cards = document.querySelectorAll('.card, .panel, .dashboard-widget');
        
        cards.forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transition = 'all 0.3s ease';
            });
        });
    }

    /**
     * Setup smooth scrolling
     */
    setupSmoothScrolling() {
        document.documentElement.style.scrollBehavior = 'smooth';
        
        // Smooth scroll for anchor links
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                const href = this.getAttribute('href');
                if (href !== '#' && href.length > 1) {
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                    }
                }
            });
        });
    }

    /**
     * Setup tooltips
     */
    setupTooltips() {
        const tooltipElements = document.querySelectorAll('[data-tooltip]');
        
        tooltipElements.forEach(element => {
            element.addEventListener('mouseenter', (e) => {
                this.showTooltip(e, element);
            });
            
            element.addEventListener('mouseleave', () => {
                this.hideTooltip();
            });
        });
    }

    /**
     * Show tooltip
     */
    showTooltip(event, element) {
        const tooltip = document.createElement('div');
        tooltip.className = 'modern-tooltip';
        tooltip.textContent = element.dataset.tooltip;
        tooltip.style.position = 'absolute';
        tooltip.style.background = 'rgba(0, 0, 0, 0.9)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '0.5rem 0.75rem';
        tooltip.style.borderRadius = '0.375rem';
        tooltip.style.fontSize = '0.875rem';
        tooltip.style.pointerEvents = 'none';
        tooltip.style.zIndex = '10000';
        tooltip.style.opacity = '0';
        tooltip.style.transition = 'opacity 0.2s';
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 8 + 'px';
        
        setTimeout(() => {
            tooltip.style.opacity = '1';
        }, 10);
        
        element._tooltip = tooltip;
    }

    /**
     * Hide tooltip
     */
    hideTooltip() {
        const tooltips = document.querySelectorAll('.modern-tooltip');
        tooltips.forEach(tooltip => {
            tooltip.style.opacity = '0';
            setTimeout(() => tooltip.remove(), 200);
        });
    }

    /**
     * Setup entrance animations
     */
    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe cards and sections
        document.querySelectorAll('.card, .panel, .form-section').forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + K for search
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('input[type="search"], .navbar-search input');
                if (searchInput) {
                    searchInput.focus();
                }
            }

            // Escape to close modals
            if (e.key === 'Escape') {
                const modals = document.querySelectorAll('.modal.show');
                modals.forEach(modal => {
                    const closeBtn = modal.querySelector('[data-dismiss="modal"]');
                    if (closeBtn) closeBtn.click();
                });
            }
        });
    }

    /**
     * Observe theme changes and apply updates
     */
    observeThemeChanges() {
        // Watch for dynamic content changes
        const observer = new MutationObserver(() => {
            // Re-apply enhancements to new elements
            this.enhanceButtons();
            this.enhanceForms();
            this.enhanceTables();
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });
    }

    /**
     * Show notification toast
     */
    showNotification(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `modern-toast modern-toast-${type}`;
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            z-index: 10000;
            animation: slideInRight 0.3s ease-out;
            max-width: 400px;
        `;

        // Add type-specific styling
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };
        toast.style.borderLeft = `4px solid ${colors[type] || colors.info}`;

        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateX(100%)';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

// Initialize Modern ERP UI when script loads
const modernERPUI = new ModernERPUI();

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ModernERPUI;
}

// Make available globally
window.ModernERPUI = ModernERPUI;

