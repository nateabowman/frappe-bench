// Table and List Enhancements for Construction Management

frappe.provide("nexelya.tables");

// Initialize table enhancements
nexelya.tables.init = function() {
  nexelya.tables.enhanceTables();
  nexelya.tables.addStatusIndicators();
  nexelya.tables.addQuickFilters();
  nexelya.tables.enhanceMobileTables();
};

// Enhance all data tables
nexelya.tables.enhanceTables = function() {
  const tables = document.querySelectorAll('.list-container table, .datatable, .frappe-list table');
  
  tables.forEach(table => {
    if (table.dataset.nexelyaEnhanced) return;
    table.dataset.nexelyaEnhanced = 'true';
    
    // Add construction-specific styling
    table.classList.add('nexelya-enhanced-table');
    
    // Enhance table headers
    const thead = table.querySelector('thead');
    if (thead) {
      thead.classList.add('nexelya-table-header');
    }
    
    // Add row hover effects
    const rows = table.querySelectorAll('tbody tr');
    rows.forEach(row => {
      row.addEventListener('mouseenter', function() {
        this.style.backgroundColor = 'var(--bg-hover)';
      });
      row.addEventListener('mouseleave', function() {
        this.style.backgroundColor = '';
      });
    });
  });
};

// Add status indicators to table cells
nexelya.tables.addStatusIndicators = function() {
  const statusCells = document.querySelectorAll('td[data-field="status"], .status-cell');
  
  statusCells.forEach(cell => {
    const text = cell.textContent.trim().toLowerCase();
    const statusIndicator = document.createElement('span');
    statusIndicator.className = 'status-indicator';
    
    if (text.includes('on schedule') || text.includes('completed') || text.includes('success')) {
      statusIndicator.classList.add('status-indicator-on-schedule');
    } else if (text.includes('at risk') || text.includes('warning') || text.includes('pending')) {
      statusIndicator.classList.add('status-indicator-at-risk');
    } else if (text.includes('delayed') || text.includes('failed') || text.includes('error')) {
      statusIndicator.classList.add('status-indicator-delayed');
    } else if (text.includes('not started') || text.includes('draft')) {
      statusIndicator.classList.add('status-indicator-not-started');
    }
    
    if (statusIndicator.classList.length > 1) {
      cell.insertBefore(statusIndicator, cell.firstChild);
    }
  });
};

// Add quick filters for common views
nexelya.tables.addQuickFilters = function() {
  const listContainer = document.querySelector('.list-container, .frappe-list');
  if (!listContainer || listContainer.querySelector('.nexelya-quick-filters')) return;
  
  const quickFilters = document.createElement('div');
  quickFilters.className = 'nexelya-quick-filters';
  quickFilters.style.cssText = `
    display: flex;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
    flex-wrap: wrap;
  `;
  
  const filters = [
    { label: 'Active Jobs', filter: { status: ['!=', 'Completed'] } },
    { label: 'This Week', filter: { creation: ['>=', frappe.datetime.add_days(frappe.datetime.get_today(), -7)] } },
    { label: 'At Risk', filter: { status: 'At Risk' } },
    { label: 'Delayed', filter: { status: 'Delayed' } }
  ];
  
  filters.forEach(filter => {
    const btn = document.createElement('button');
    btn.className = 'btn btn-sm btn-secondary';
    btn.textContent = filter.label;
    btn.onclick = () => {
      // Apply filter
      if (window.frappe && frappe.list_view) {
        frappe.list_view.filter_area.add(filter.filter);
      }
    };
    quickFilters.appendChild(btn);
  });
  
  listContainer.insertBefore(quickFilters, listContainer.firstChild);
};

// Enhance tables for mobile (card view)
nexelya.tables.enhanceMobileTables = function() {
  if (window.innerWidth > 768) return;
  
  const tables = document.querySelectorAll('.list-container table, .datatable');
  tables.forEach(table => {
    // Convert to card view on mobile
    if (!table.classList.contains('nexelya-mobile-cards')) {
      table.classList.add('nexelya-mobile-cards');
      
      // Add data-label attributes for mobile display
      const headers = table.querySelectorAll('thead th');
      const headerTexts = Array.from(headers).map(th => th.textContent.trim());
      
      const rows = table.querySelectorAll('tbody tr');
      rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        cells.forEach((cell, index) => {
          if (headerTexts[index]) {
            cell.setAttribute('data-label', headerTexts[index]);
          }
        });
      });
    }
  });
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', nexelya.tables.init);
} else {
  nexelya.tables.init();
}

// Re-initialize on route changes
if (frappe.router) {
  frappe.router.on("change", () => {
    setTimeout(nexelya.tables.init, 500);
  });
}

// Watch for new tables added dynamically
if (window.MutationObserver) {
  const observer = new MutationObserver(() => {
    nexelya.tables.init();
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}

