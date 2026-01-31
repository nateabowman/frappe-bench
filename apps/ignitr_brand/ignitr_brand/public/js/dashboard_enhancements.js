// Dashboard Enhancements for Construction Management

frappe.provide("nexelya.dashboard");

// Construction-specific dashboard widgets
nexelya.dashboard.init = function() {
  // Initialize dashboard enhancements when dashboard loads
  if (frappe.router && frappe.router.current_route) {
    const route = frappe.router.current_route[0];
    if (route && route.name && route.name.includes('Dashboard')) {
      nexelya.dashboard.enhanceDashboard();
    }
  }
  
  // Also run on route changes
  if (frappe.router) {
    frappe.router.on("change", () => {
      setTimeout(() => {
        nexelya.dashboard.enhanceDashboard();
      }, 500);
    });
  }
};

// Enhance dashboard with construction-specific features
nexelya.dashboard.enhanceDashboard = function() {
  // Add KPI cards styling
  nexelya.dashboard.enhanceKPICards();
  
  // Add status indicators
  nexelya.dashboard.enhanceStatusIndicators();
  
  // Add quick actions
  nexelya.dashboard.addQuickActions();
};

// Enhance KPI cards
nexelya.dashboard.enhanceKPICards = function() {
  const kpiCards = document.querySelectorAll('.number-card, .metric-card');
  kpiCards.forEach(card => {
    if (!card.classList.contains('nexelya-enhanced')) {
      card.classList.add('kpi-card', 'nexelya-enhanced');
      
      // Add hover effect
      card.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-2px)';
        this.style.boxShadow = 'var(--shadow-md)';
      });
      
      card.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = 'var(--shadow-sm)';
      });
    }
  });
};

// Enhance status indicators
nexelya.dashboard.enhanceStatusIndicators = function() {
  // Find status badges and enhance them
  const statusBadges = document.querySelectorAll('.indicator-pill, .status-badge');
  statusBadges.forEach(badge => {
    const text = badge.textContent.trim().toLowerCase();
    
    // Map statuses to colors
    if (text.includes('on schedule') || text.includes('completed') || text.includes('success')) {
      badge.classList.add('badge-status-on-schedule');
    } else if (text.includes('at risk') || text.includes('warning') || text.includes('pending')) {
      badge.classList.add('badge-status-at-risk');
    } else if (text.includes('delayed') || text.includes('failed') || text.includes('error')) {
      badge.classList.add('badge-status-delayed');
    } else if (text.includes('not started') || text.includes('draft')) {
      badge.classList.add('badge-status-not-started');
    }
  });
};

// Add quick action buttons
nexelya.dashboard.addQuickActions = function() {
  // This will be enhanced based on the specific dashboard context
  const dashboardContainer = document.querySelector('.dashboard-container, .workspace-content');
  if (dashboardContainer && !dashboardContainer.querySelector('.nexelya-quick-actions')) {
    const quickActions = document.createElement('div');
    quickActions.className = 'nexelya-quick-actions';
    quickActions.style.cssText = 'display: flex; gap: var(--spacing-sm); margin-bottom: var(--spacing-lg); flex-wrap: wrap;';
    
    // Add common quick actions based on context
    const actions = nexelya.dashboard.getQuickActions();
    actions.forEach(action => {
      const btn = document.createElement('button');
      btn.className = 'btn btn-primary btn-sm';
      btn.textContent = action.label;
      btn.onclick = action.onclick;
      quickActions.appendChild(btn);
    });
    
    if (actions.length > 0) {
      dashboardContainer.insertBefore(quickActions, dashboardContainer.firstChild);
    }
  }
};

// Get quick actions based on current context
nexelya.dashboard.getQuickActions = function() {
  const actions = [];
  const route = frappe.router.current_route;
  
  // Add context-specific actions
  if (route && route[0]) {
    const routeName = route[0].name || '';
    
    if (routeName.includes('Project') || routeName.includes('Job Site')) {
      actions.push({
        label: 'New Job Site',
        onclick: () => frappe.set_route('Form', 'Project', 'new')
      });
      actions.push({
        label: 'View All Job Sites',
        onclick: () => frappe.set_route('List', 'Project')
      });
    }
    
    if (routeName.includes('RFI')) {
      actions.push({
        label: 'New RFI',
        onclick: () => frappe.set_route('Form', 'RFI', 'new')
      });
    }
    
    if (routeName.includes('Daily Log')) {
      actions.push({
        label: 'New Daily Log',
        onclick: () => frappe.set_route('Form', 'Daily Log', 'new')
      });
    }
  }
  
  return actions;
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nexelya.dashboard.init);
} else {
  nexelya.dashboard.init();
}

