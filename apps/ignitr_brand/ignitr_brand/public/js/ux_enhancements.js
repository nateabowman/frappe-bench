// UX Enhancements for Construction Management

frappe.provide("nexelya.ux");

// Initialize UX enhancements
nexelya.ux.init = function() {
  nexelya.ux.setupKeyboardShortcuts();
  nexelya.ux.enhanceSearch();
  nexelya.ux.addRecentItems();
  nexelya.ux.addFavorites();
  nexelya.ux.setupNotifications();
  nexelya.ux.addHelpTooltips();
  nexelya.ux.addPWAFeatures();
};

// Keyboard shortcuts for power users
nexelya.ux.setupKeyboardShortcuts = function() {
  document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + K for quick search
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      nexelya.ux.openQuickSearch();
    }
    
    // Ctrl/Cmd + N for new document (context-aware)
    if ((e.ctrlKey || e.metaKey) && e.key === 'n' && !e.target.matches('input, textarea')) {
      e.preventDefault();
      nexelya.ux.createNewDocument();
    }
    
    // Escape to close modals
    if (e.key === 'Escape') {
      const modals = document.querySelectorAll('.modal.show, .dialog.show');
      modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close, [data-dismiss="modal"]');
        if (closeBtn) closeBtn.click();
      });
    }
  });
};

// Open quick search
nexelya.ux.openQuickSearch = function() {
  // Use Frappe's built-in search if available
  if (frappe.search && frappe.search.toggle) {
    frappe.search.toggle();
  } else {
    // Fallback: focus on search input
    const searchInput = document.querySelector('input[type="search"], input[placeholder*="Search"]');
    if (searchInput) {
      searchInput.focus();
      searchInput.select();
    }
  }
};

// Create new document (context-aware)
nexelya.ux.createNewDocument = function() {
  const route = frappe.router.current_route;
  if (route && route[0] && route[0].name) {
    const doctype = route[0].name;
    if (doctype && doctype !== 'Desktop') {
      frappe.set_route('Form', doctype, 'new');
    }
  }
};

// Enhance search with construction terminology
nexelya.ux.enhanceSearch = function() {
  const searchInputs = document.querySelectorAll('input[type="search"], input[placeholder*="Search"]');
  
  searchInputs.forEach(input => {
    // Add construction-specific search suggestions
    input.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase();
      if (query.length > 2) {
        nexelya.ux.showSearchSuggestions(query, input);
      }
    });
  });
};

// Show search suggestions
nexelya.ux.showSearchSuggestions = function(query, input) {
  // This would integrate with Frappe's search API
  // For now, just enhance the search experience
  const suggestions = [
    'Job Site',
    'RFI',
    'Submittal',
    'Daily Log',
    'Equipment',
    'Safety Incident',
    'Punch List'
  ].filter(item => item.toLowerCase().includes(query));
  
  // Would display suggestions in a dropdown
};

// Recent items quick access
nexelya.ux.addRecentItems = function() {
  // Store recent items in localStorage
  if (frappe.router) {
    frappe.router.on("change", () => {
      const route = frappe.router.current_route;
      if (route && route[0]) {
        const item = {
          doctype: route[0].name,
          name: route[0].name || 'new',
          timestamp: Date.now()
        };
        
        let recent = JSON.parse(localStorage.getItem('nexelya_recent_items') || '[]');
        recent = recent.filter(r => !(r.doctype === item.doctype && r.name === item.name));
        recent.unshift(item);
        recent = recent.slice(0, 10); // Keep last 10
        localStorage.setItem('nexelya_recent_items', JSON.stringify(recent));
      }
    });
  }
};

// Favorites/bookmarks
nexelya.ux.addFavorites = function() {
  // Add favorite button to document headers
  const addFavoriteButton = () => {
    const docHeader = document.querySelector('.page-head, .form-head');
    if (docHeader && !docHeader.querySelector('.nexelya-favorite-btn')) {
      const route = frappe.router.current_route;
      if (route && route[0] && route[0].name) {
        const favoriteBtn = document.createElement('button');
        favoriteBtn.className = 'btn btn-sm btn-secondary nexelya-favorite-btn';
        favoriteBtn.innerHTML = '<i class="fa fa-star"></i>';
        favoriteBtn.title = 'Add to Favorites';
        
        const favorites = JSON.parse(localStorage.getItem('nexelya_favorites') || '[]');
        const isFavorite = favorites.some(f => 
          f.doctype === route[0].name && f.name === (route[0].name || 'new')
        );
        
        if (isFavorite) {
          favoriteBtn.classList.add('active');
          favoriteBtn.innerHTML = '<i class="fa fa-star"></i>';
        }
        
        favoriteBtn.addEventListener('click', () => {
          nexelya.ux.toggleFavorite(route[0].name, route[0].name || 'new', favoriteBtn);
        });
        
        docHeader.appendChild(favoriteBtn);
      }
    }
  };
  
  if (frappe.router) {
    frappe.router.on("change", () => {
      setTimeout(addFavoriteButton, 500);
    });
  }
  
  addFavoriteButton();
};

// Toggle favorite
nexelya.ux.toggleFavorite = function(doctype, name, button) {
  let favorites = JSON.parse(localStorage.getItem('nexelya_favorites') || '[]');
  const index = favorites.findIndex(f => f.doctype === doctype && f.name === name);
  
  if (index > -1) {
    favorites.splice(index, 1);
    button.classList.remove('active');
    button.innerHTML = '<i class="fa fa-star-o"></i>';
    frappe.show_alert({ message: 'Removed from favorites', indicator: 'blue' });
  } else {
    favorites.push({ doctype, name, timestamp: Date.now() });
    button.classList.add('active');
    button.innerHTML = '<i class="fa fa-star"></i>';
    frappe.show_alert({ message: 'Added to favorites', indicator: 'green' });
  }
  
  localStorage.setItem('nexelya_favorites', JSON.stringify(favorites));
};

// Setup notifications
nexelya.ux.setupNotifications = function() {
  // Create notification center
  const notificationCenter = document.createElement('div');
  notificationCenter.className = 'nexelya-notification-center';
  notificationCenter.style.cssText = `
    position: fixed;
    top: var(--header-height);
    right: var(--spacing-md);
    width: 350px;
    max-height: 500px;
    overflow-y: auto;
    background: var(--bg-primary);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    z-index: var(--z-popover);
    display: none;
    padding: var(--spacing-md);
  `;
  
  document.body.appendChild(notificationCenter);
  
  // Add notification button to navbar
  const addNotificationButton = () => {
    const navbar = document.querySelector('.navbar, .desk-navbar');
    if (navbar && !navbar.querySelector('.nexelya-notification-btn')) {
      const notifBtn = document.createElement('button');
      notifBtn.className = 'btn btn-sm btn-secondary nexelya-notification-btn';
      notifBtn.innerHTML = '<i class="fa fa-bell"></i>';
      notifBtn.title = 'Notifications';
      
      // Check for unread count
      const unreadCount = nexelya.ux.getUnreadNotificationCount();
      if (unreadCount > 0) {
        const badge = document.createElement('span');
        badge.className = 'badge badge-danger';
        badge.textContent = unreadCount;
        badge.style.cssText = 'position: absolute; top: -5px; right: -5px;';
        notifBtn.style.position = 'relative';
        notifBtn.appendChild(badge);
      }
      
      notifBtn.addEventListener('click', () => {
        notificationCenter.style.display = notificationCenter.style.display === 'none' ? 'block' : 'none';
        nexelya.ux.loadNotifications(notificationCenter);
      });
      
      navbar.appendChild(notifBtn);
    }
  };
  
  addNotificationButton();
  
  // Load notifications periodically
  setInterval(() => {
    nexelya.ux.loadNotifications(notificationCenter);
  }, 60000); // Every minute
};

// Get unread notification count
nexelya.ux.getUnreadNotificationCount = function() {
  // This would integrate with Frappe's notification system
  // For now, return 0
  return 0;
};

// Load notifications
nexelya.ux.loadNotifications = function(container) {
  // This would fetch from Frappe's notification API
  // For now, show placeholder
  container.innerHTML = '<div class="text-center text-muted p-3">No new notifications</div>';
};

// Add help tooltips with construction context
nexelya.ux.addHelpTooltips = function() {
  // Add help icons to form fields
  const addHelpIcons = () => {
    const helpFields = document.querySelectorAll('[data-help], [data-description]');
    helpFields.forEach(field => {
      if (!field.querySelector('.nexelya-help-icon')) {
        const helpIcon = document.createElement('i');
        helpIcon.className = 'fa fa-question-circle nexelya-help-icon';
        helpIcon.style.cssText = `
          color: var(--nexelya-info);
          cursor: help;
          margin-left: var(--spacing-xs);
          font-size: var(--font-size-sm);
        `;
        helpIcon.title = field.dataset.help || field.dataset.description || 'Help';
        
        helpIcon.addEventListener('click', (e) => {
          e.stopPropagation();
          nexelya.ux.showHelpTooltip(field, helpIcon);
        });
        
        const label = field.closest('.form-group')?.querySelector('label');
        if (label) {
          label.appendChild(helpIcon);
        }
      }
    });
  };
  
  if (frappe.router) {
    frappe.router.on("change", () => {
      setTimeout(addHelpIcons, 500);
    });
  }
  
  addHelpIcons();
};

// Show help tooltip
nexelya.ux.showHelpTooltip = function(field, icon) {
  const tooltip = document.createElement('div');
  tooltip.className = 'nexelya-help-tooltip';
  tooltip.style.cssText = `
    position: absolute;
    background: var(--bg-primary);
    border: 1px solid var(--border-primary);
    border-radius: var(--radius-md);
    padding: var(--spacing-md);
    box-shadow: var(--shadow-lg);
    z-index: var(--z-tooltip);
    max-width: 300px;
    font-size: var(--font-size-sm);
  `;
  tooltip.textContent = field.dataset.help || field.dataset.description || 'Help information';
  
  const rect = icon.getBoundingClientRect();
  tooltip.style.top = (rect.bottom + 5) + 'px';
  tooltip.style.left = rect.left + 'px';
  
  document.body.appendChild(tooltip);
  
  // Remove on click outside
  setTimeout(() => {
    document.addEventListener('click', function removeTooltip() {
      tooltip.remove();
      document.removeEventListener('click', removeTooltip);
    });
  }, 100);
};


// PWA features
nexelya.ux.addPWAFeatures = function() {
  // Service worker registration (would need actual service worker file)
  if ('serviceWorker' in navigator) {
    // Service worker would be registered here
  }
  
  // Install prompt
  let deferredPrompt;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    nexelya.ux.showInstallPrompt();
  });
  
  // Show install prompt
  window.nexelyaShowInstallPrompt = function() {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      deferredPrompt.userChoice.then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          frappe.show_alert({ message: 'App installed', indicator: 'green' });
        }
        deferredPrompt = null;
      });
    }
  };
};

// Show install prompt UI
nexelya.ux.showInstallPrompt = function() {
  const prompt = document.createElement('div');
  prompt.className = 'pwa-install-prompt';
  prompt.innerHTML = `
    <div class="pwa-install-prompt-header">
      <div class="pwa-install-prompt-title">Install Nexelya</div>
      <button class="pwa-install-prompt-close">&times;</button>
    </div>
    <p>Install Nexelya as an app for a better experience on your device.</p>
    <div class="pwa-install-prompt-actions">
      <button class="btn btn-primary" onclick="nexelyaShowInstallPrompt()">Install</button>
      <button class="btn btn-secondary pwa-install-prompt-close">Not Now</button>
    </div>
  `;
  
  document.body.appendChild(prompt);
  
  prompt.querySelectorAll('.pwa-install-prompt-close').forEach(btn => {
    btn.addEventListener('click', () => {
      prompt.remove();
    });
  });
  
  // Show after delay
  setTimeout(() => {
    prompt.classList.add('show');
  }, 5000);
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nexelya.ux.init);
} else {
  nexelya.ux.init();
}

