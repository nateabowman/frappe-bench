// Navigation Enhancements for Construction Management

frappe.provide("nexelya.navigation");

// Initialize navigation enhancements
nexelya.navigation.init = function() {
  nexelya.navigation.enhanceSidebar();
  nexelya.navigation.addModuleGrouping();
  nexelya.navigation.enhanceMobileNavigation();
};

// Enhance sidebar with construction module grouping
nexelya.navigation.enhanceSidebar = function() {
  // Wait for sidebar to load
  setTimeout(() => {
    const sidebar = document.querySelector('.sidebar, .desk-sidebar, .module-sidebar');
    if (!sidebar) return;
    
    // Add construction module categories
    const moduleCategories = {
      'field-operations': {
        label: 'Field Operations',
        modules: ['Job Sites', 'Daily Log', 'Equipment & Fleet', 'Equipment'],
        color: 'var(--nexelya-success)'
      },
      'project-management': {
        label: 'Project Management',
        modules: ['RFI', 'Submittal', 'Project Schedule', 'Schedule'],
        color: 'var(--nexelya-primary)'
      },
      'financial': {
        label: 'Financial',
        modules: ['Contract', 'Contracts', 'Invoice', 'Invoices', 'WIP Report', 'Retainage'],
        color: 'var(--nexelya-secondary)'
      },
      'resources': {
        label: 'Resources',
        modules: ['Crew', 'Crew Member', 'Materials & Inventory', 'Materials', 'Equipment & Fleet'],
        color: 'var(--nexelya-warning)'
      },
      'quality-safety': {
        label: 'Quality & Safety',
        modules: ['Inspection Form', 'Punch List', 'Safety Incident', 'OSHA Compliance'],
        color: 'var(--nexelya-danger)'
      }
    };
    
    // Group modules by category
    Object.keys(moduleCategories).forEach(categoryKey => {
      const category = moduleCategories[categoryKey];
      const moduleCards = Array.from(sidebar.querySelectorAll('.module-card, .module-link'));
      
      moduleCards.forEach(card => {
        const label = card.textContent.trim() || card.getAttribute('data-label') || '';
        const matchesCategory = category.modules.some(module => 
          label.includes(module) || label === module
        );
        
        if (matchesCategory) {
          card.setAttribute('data-category', categoryKey);
          card.style.borderLeftColor = category.color;
          
          // Add category badge
          if (!card.querySelector('.module-category-badge')) {
            const badge = document.createElement('span');
            badge.className = 'module-category-badge';
            badge.textContent = category.label;
            badge.style.cssText = `
              font-size: var(--font-size-xs);
              font-weight: var(--font-weight-semibold);
              text-transform: uppercase;
              letter-spacing: 0.5px;
              color: var(--text-tertiary);
              margin-top: var(--spacing-xs);
            `;
            card.appendChild(badge);
          }
        }
      });
    });
  }, 1000);
};

// Add module grouping headers
nexelya.navigation.addModuleGrouping = function() {
  const sidebar = document.querySelector('.sidebar, .desk-sidebar, .module-sidebar');
  if (!sidebar) return;
  
  const groups = [
    { id: 'field-operations', label: 'Field Operations', modules: ['Job Sites', 'Daily Log', 'Equipment'] },
    { id: 'project-management', label: 'Project Management', modules: ['RFI', 'Submittal', 'Schedule'] },
    { id: 'financial', label: 'Financial', modules: ['Contract', 'Invoice', 'WIP Report'] },
    { id: 'resources', label: 'Resources', modules: ['Crew', 'Materials', 'Equipment & Fleet'] },
    { id: 'quality-safety', label: 'Quality & Safety', modules: ['Inspection', 'Punch List', 'Safety'] }
  ];
  
  // This would reorganize modules into groups
  // Implementation depends on Frappe's sidebar structure
};

// Enhance mobile navigation
nexelya.navigation.enhanceMobileNavigation = function() {
  if (window.innerWidth > 768) return;
  
  // Convert sidebar to bottom navigation on mobile
  const sidebar = document.querySelector('.sidebar, .desk-sidebar');
  if (sidebar) {
    sidebar.classList.add('mobile-bottom-nav');
    
    // Show only frequently used modules on mobile
    const allModules = sidebar.querySelectorAll('.module-card, .module-link');
    const frequentModules = Array.from(allModules).slice(0, 5); // Top 5
    
    allModules.forEach((module, index) => {
      if (index >= 5) {
        module.style.display = 'none';
      }
    });
    
    // Add "More" button
    const moreBtn = document.createElement('button');
    moreBtn.className = 'btn btn-sm btn-secondary';
    moreBtn.textContent = 'More';
    moreBtn.onclick = () => {
      // Show all modules in a modal
      nexelya.navigation.showAllModulesModal();
    };
    sidebar.appendChild(moreBtn);
  }
};

// Show all modules in a modal
nexelya.navigation.showAllModulesModal = function() {
  const dialog = new frappe.ui.Dialog({
    title: __('All Modules'),
    fields: [
      {
        fieldtype: 'HTML',
        options: '<div id="all-modules-list"></div>'
      }
    ]
  });
  
  dialog.show();
  
  // Populate with all modules
  const modulesList = dialog.$wrapper.find('#all-modules-list');
  // Implementation would list all modules here
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nexelya.navigation.init);
} else {
  nexelya.navigation.init();
}

// Re-initialize on route changes
if (frappe.router) {
  frappe.router.on("change", () => {
    setTimeout(nexelya.navigation.init, 500);
  });
}

