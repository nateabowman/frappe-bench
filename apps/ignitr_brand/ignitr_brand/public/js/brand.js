// ensure namespace
frappe.provide("ignitr_brand");

// Comprehensive brand replacement configuration for US Construction Companies
ignitr_brand.brandConfig = {
  replacements: [
    // Core Branding - ORDER MATTERS: More specific first
    { from: /ERPNext/gi, to: "Nexelya" },
    { from: /Frappe Framework/gi, to: "Nexelya Platform" },
    { from: /Frappe CRM/gi, to: "Nexelya CRM" },
    { from: /Frappe Cloud/gi, to: "Nexelya Cloud" },
    { from: /Frappe Desk/gi, to: "Nexelya Dashboard" },
    { from: /Frappe HR/gi, to: "Nexelya Workforce" },
    { from: /Frappe Bench/gi, to: "Nexelya CLI" },
    { from: /Frappe API/gi, to: "Nexelya API" },
    { from: /Frappe Chat/gi, to: "Nexelya Chat" },
    { from: /Frappe Integrations/gi, to: "Nexelya Integrations" },
    { from: /Frappe App/gi, to: "Nexelya App" },
    { from: /Frappe Site/gi, to: "Nexelya Site" },
    { from: /Frappe Support/gi, to: "Nexelya Support" },
    { from: /Frappe Help/gi, to: "Nexelya Help" },
    { from: /Frappe Developer/gi, to: "Nexelya Developer" },
    { from: /Frappe Developer API/gi, to: "Nexelya Developer API" },
    { from: /Frappe/gi, to: "Nexelya" },
    
    // Construction-Specific Module Renaming
    { from: /Projects/gi, to: "Job Sites" },
    { from: /Project/gi, to: "Job Site" },
    { from: /Buying/gi, to: "Procurement" },
    { from: /Selling/gi, to: "Estimating & Billing" },
    { from: /Stock/gi, to: "Materials & Inventory" },
    { from: /Warehouse/gi, to: "Yard" },
    { from: /Warehouses/gi, to: "Yards" },
    { from: /Manufacturing/gi, to: "Prefab & Modular" },
    { from: /Assets/gi, to: "Equipment & Fleet" },
    // Handle "Asset Maintenance" as a single unit FIRST to prevent "Equipment Equipment Maintenance"
    { from: /\bAsset\s+Maintenance\b/gi, to: "Equipment Maintenance" },
    { from: /\bAsset\b(?!\s*&)/gi, to: "Equipment" }, // Word boundary, but not if followed by "&" (Equipment & Fleet)
    // Maintenance replacement - only if not already "Equipment Maintenance" and not preceded by "Equipment"
    { from: /(?<!Equipment\s)\bMaintenance\b/gi, to: "Equipment Maintenance" },
    // Handle "Customer Support" as a single unit FIRST to prevent duplication
    { from: /\bCustomer\s+Support\b/gi, to: "Client Support" },
    // Support replacement - only if not already "Client Support" and not part of another phrase
    { from: /(?<!Client\s)(?<!Customer\s)\bSupport\b(?!\s+Client)/gi, to: "Client Support" },
    { from: /CRM/gi, to: "CRM" },
    
    // Construction Terminology - Use word boundaries to prevent double replacement
    // Customer -> Client, but skip if already processed above
    { from: /\bCustomer\b/gi, to: "Client" },
    { from: /\bCustomers\b/gi, to: "Clients" },
    { from: /Supplier/gi, to: "Vendor" },
    { from: /Suppliers/gi, to: "Vendors" },
    { from: /Sales Order/gi, to: "Contract" },
    { from: /Sales Orders/gi, to: "Contracts" },
    { from: /Purchase Order/gi, to: "Purchase Order" },
    { from: /Purchase Orders/gi, to: "Purchase Orders" },
    { from: /Quotation/gi, to: "Estimate" },
    { from: /Quotations/gi, to: "Estimates" },
    { from: /Sales Invoice/gi, to: "Invoice" },
    { from: /Sales Invoices/gi, to: "Invoices" },
    { from: /Delivery Note/gi, to: "Delivery Ticket" },
    { from: /Delivery Notes/gi, to: "Delivery Tickets" },
    { from: /Item/gi, to: "Material" },
    { from: /Items/gi, to: "Materials" },
    { from: /Work Order/gi, to: "Work Order" },
    { from: /Work Orders/gi, to: "Work Orders" },
    { from: /Timesheet/gi, to: "Time Card" },
    { from: /Timesheets/gi, to: "Time Cards" },
    { from: /Employee/gi, to: "Crew Member" },
    { from: /Employees/gi, to: "Crew" },
    
    // Remove Branding
    { from: /Powered by ERPNext/gi, to: "" },
    { from: /Powered by Frappe/gi, to: "" },
    { from: /Built on Frappe/gi, to: "" },
    { from: /Built with Frappe/gi, to: "" },
    
    // Construction-Specific Welcome Messages
    { from: /Let's begin your journey with ERPNext/gi, to: "Build smarter. Manage better. Grow faster." },
    { from: /Welcome to ERPNext/gi, to: "Welcome to Nexelya" },
    { from: /Welcome to Frappe/gi, to: "Welcome to Nexelya" },
  ]
};

// Track processed nodes to avoid re-processing
ignitr_brand.processedNodes = new WeakSet();

// Check if text needs processing (contains original terms that should be replaced)
ignitr_brand.needsProcessing = (text) => {
  if (!text || typeof text !== 'string') return false;
  
  // Check if text contains any original terms that need replacement
  const originalTerms = /(Frappe|ERPNext|Customer|Customers|Project|Projects|Asset|Assets|Warehouse|Warehouses|Stock|Buying|Selling|Supplier|Suppliers|Sales Order|Sales Orders|Quotation|Quotations|Sales Invoice|Sales Invoices|Delivery Note|Delivery Notes|Item|Items|Timesheet|Timesheets|Employee|Employees|Manufacturing|Maintenance|Support|CRM)/i;
  return originalTerms.test(text);
};

// Check if text is already processed (contains branded terms and no original terms)
ignitr_brand.isAlreadyProcessed = (text) => {
  if (!text || typeof text !== 'string') return false;
  
    // If it has branded terms but no original terms, it's already processed
    const hasBrandedTerms = /(Nexelya|Job Site|Job Sites|Equipment|Equipment & Fleet|Materials & Inventory|Procurement|Estimating & Billing|Client|Clients|Vendor|Vendors|Contract|Contracts|Estimate|Estimates|Invoice|Invoices|Delivery Ticket|Delivery Tickets|Material|Materials|Time Card|Time Cards|Crew Member|Crew|Equipment Maintenance|Client Support|Yard|Yards|Prefab & Modular)/i.test(text);
    const hasOriginalTerms = /(Frappe|ERPNext|Customer|Customers|Project|Projects|Asset|Assets|Warehouse|Warehouses|Stock|Buying|Selling|Supplier|Suppliers|Sales Order|Sales Orders|Quotation|Quotations|Sales Invoice|Sales Invoices|Delivery Note|Delivery Notes|Item|Items|Timesheet|Timesheets|Employee|Employees|Manufacturing|Maintenance|Support|CRM)/i.test(text);
    
    // Special check: if text has "Client Client" or "Equipment Equipment", it's a duplicate and needs fixing
    if (/\bClient\s+Client\b/i.test(text) || /\bEquipment\s+Equipment\b/i.test(text)) {
      return false; // Not already processed, needs fixing
    }
  
  return hasBrandedTerms && !hasOriginalTerms;
};

// Remove the "Browse Apps" module card
ignitr_brand.hideBrowseApps = () => {
  const card = document.querySelector('.module-card[data-label="Browse Apps"]');
  if (card) card.remove();
};

// Hide Frappe/ERPNext footer links
ignitr_brand.hideBrandingFooters = () => {
  // Hide "Powered by" and "Built on" footer elements
  const footerLinks = document.querySelectorAll('footer a[href*="frappe"], footer a[href*="erpnext"]');
  footerLinks.forEach(link => {
    const parent = link.closest('div, span, p');
    if (parent && (parent.textContent.includes('Powered by') || parent.textContent.includes('Built on'))) {
      parent.style.display = 'none';
    }
  });
  
  // Hide any text nodes containing branding
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    null,
    false
  );
  
  let node;
  while (node = walker.nextNode()) {
    const text = node.textContent;
    if (text.match(/Powered by (Frappe|ERPNext)|Built on Frappe/i)) {
      const parent = node.parentElement;
      if (parent && (parent.tagName === 'SPAN' || parent.tagName === 'DIV' || parent.tagName === 'P')) {
        parent.style.display = 'none';
      }
    }
  }
};

// Comprehensive label replacement - SIMPLIFIED to prevent duplicates
ignitr_brand.replaceLabels = () => {
  const walker = document.createTreeWalker(
    document.body,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: function(node) {
        // Skip script and style nodes
        const parent = node.parentElement;
        if (!parent || parent.tagName === 'SCRIPT' || parent.tagName === 'STYLE') {
          return NodeFilter.FILTER_REJECT;
        }
        // Skip if already processed
        if (ignitr_brand.processedNodes.has(node)) {
          return NodeFilter.FILTER_REJECT;
        }
        // Skip if parent is marked as processed
        if (parent && parent.hasAttribute('data-ignitr-processed')) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    },
    false
  );
  
  let node;
  while (node = walker.nextNode()) {
    let text = node.textContent;
    
    // Skip if empty
    if (!text || !text.trim()) {
      ignitr_brand.processedNodes.add(node);
      continue;
    }
    
    // Skip if already processed (has branded terms, no original terms)
    if (ignitr_brand.isAlreadyProcessed(text)) {
      ignitr_brand.processedNodes.add(node);
      if (node.parentElement) {
        node.parentElement.setAttribute('data-ignitr-processed', 'true');
      }
      continue;
    }
    
    // Only process if it needs processing (has original terms)
    if (!ignitr_brand.needsProcessing(text)) {
      ignitr_brand.processedNodes.add(node);
      if (node.parentElement) {
        node.parentElement.setAttribute('data-ignitr-processed', 'true');
      }
      continue;
    }
    
    // First, fix any existing duplicates (cleanup pass)
    let newText = text;
    
    // Fix duplicate patterns - do this first to clean up any existing issues
    // Fix "Equipment Equipment Maintenance" -> "Equipment Maintenance" (most specific first)
    newText = newText.replace(/\bEquipment\s+Equipment\s+Maintenance\b/gi, 'Equipment Maintenance');
    // Fix "Client Client Support" -> "Client Support"
    newText = newText.replace(/\bClient\s+Client\s+Support\b/gi, 'Client Support');
    // Fix "Equipment Equipment" -> "Equipment" (but preserve "Equipment Maintenance")
    newText = newText.replace(/\bEquipment\s+Equipment\b(?!\s+Maintenance)/gi, 'Equipment');
    // Fix "Client Client" -> "Client" (but preserve "Client Support")
    newText = newText.replace(/\bClient\s+Client\b(?!\s+Support)/gi, 'Client');
    
    let changed = newText !== text;
    
    // Apply replacements - but prevent duplicates
    ignitr_brand.brandConfig.replacements.forEach(replacement => {
      const beforeReplace = newText;
      
      // Skip if replacement would create duplicates
      // Don't replace "Customer" if text already has "Client" and no "Customer" to replace
      if (replacement.to === "Client" && /\bClient\b/i.test(newText) && !/\bCustomer\b/i.test(newText)) {
        return;
      }
      // Don't replace "Asset" if text already has "Equipment" and no "Asset" to replace
      if (replacement.to === "Equipment" && /\bEquipment\b/i.test(newText) && !/\bAsset\b/i.test(newText)) {
        return;
      }
      // Don't replace "Maintenance" if text already contains "Equipment Maintenance"
      if (replacement.to === "Equipment Maintenance" && /\bEquipment\s+Maintenance\b/i.test(newText)) {
        return;
      }
      // Don't replace standalone "Maintenance" if "Equipment Maintenance" already exists
      if (replacement.to === "Equipment Maintenance") {
        // Check if "Equipment Maintenance" already exists in the text
        if (/\bEquipment\s+Maintenance\b/i.test(newText)) {
          return; // Already has "Equipment Maintenance", don't duplicate
        }
        // Check if we're replacing "Maintenance" and "Equipment" is already in the text
        // This prevents "Equipment Maintenance" -> "Equipment Equipment Maintenance"
        if (replacement.from.test(newText) && /\bEquipment\b/i.test(newText)) {
          // Test if the replacement would create a duplicate
          const testReplace = newText.replace(replacement.from, replacement.to);
          if (/\bEquipment\s+Equipment\s+Maintenance\b/i.test(testReplace)) {
            return; // Would create duplicate, skip
          }
        }
      }
      // Don't replace "Support" if text already has "Client Support"
      if (replacement.to === "Client Support") {
        // Check if "Client Support" already exists in the text
        if (/\bClient\s+Support\b/i.test(newText)) {
          return; // Already has "Client Support", don't duplicate
        }
        // Check if we're replacing "Support" and "Client" is already in the text
        // This prevents "Client Support" -> "Client Client Support"
        if (replacement.from.test(newText) && /\bClient\b/i.test(newText)) {
          // Test if the replacement would create a duplicate
          const testReplace = newText.replace(replacement.from, replacement.to);
          if (/\bClient\s+Client\s+Support\b/i.test(testReplace)) {
            return; // Would create duplicate, skip
          }
        }
      }
      
      newText = newText.replace(replacement.from, replacement.to);
      if (beforeReplace !== newText) {
        changed = true;
      }
    });
    
    // Final cleanup pass to fix any duplicates that might have been created
    const finalCleanup = newText
      .replace(/\bEquipment\s+Equipment\s+Maintenance\b/gi, 'Equipment Maintenance')
      .replace(/\bClient\s+Client\s+Support\b/gi, 'Client Support')
      .replace(/\bEquipment\s+Equipment\b(?!\s+Maintenance)/gi, 'Equipment')
      .replace(/\bClient\s+Client\b(?!\s+Support)/gi, 'Client');
    
    if (finalCleanup !== newText) {
      newText = finalCleanup;
      changed = true;
    }
    
    // Only update if changed
    if (changed && newText !== text) {
      node.textContent = newText;
    }
    
    // Mark as processed immediately
    ignitr_brand.processedNodes.add(node);
    if (node.parentElement) {
      node.parentElement.setAttribute('data-ignitr-processed', 'true');
    }
  }
  
  // Replace in title attributes
  document.querySelectorAll('[title]:not([data-ignitr-processed])').forEach(el => {
    let title = el.getAttribute('title');
    if (!title) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    // Skip if already processed
    if (ignitr_brand.isAlreadyProcessed(title)) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    // Only process if needed
    if (!ignitr_brand.needsProcessing(title)) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    let newTitle = title;
    let changed = false;
    
    ignitr_brand.brandConfig.replacements.forEach(replacement => {
      const beforeReplace = newTitle;
      newTitle = newTitle.replace(replacement.from, replacement.to);
      if (beforeReplace !== newTitle) {
        changed = true;
      }
    });
    
    if (changed && newTitle !== title) {
      el.setAttribute('title', newTitle);
    }
    el.setAttribute('data-ignitr-processed', 'true');
  });
  
  // Replace in placeholder attributes
  document.querySelectorAll('[placeholder]:not([data-ignitr-processed])').forEach(el => {
    let placeholder = el.getAttribute('placeholder');
    if (!placeholder) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    // Skip if already processed
    if (ignitr_brand.isAlreadyProcessed(placeholder)) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    // Only process if needed
    if (!ignitr_brand.needsProcessing(placeholder)) {
      el.setAttribute('data-ignitr-processed', 'true');
      return;
    }
    
    // First, fix any existing duplicates (cleanup pass)
    let newPlaceholder = placeholder;
    newPlaceholder = newPlaceholder
      .replace(/\bEquipment\s+Equipment\s+Maintenance\b/gi, 'Equipment Maintenance')
      .replace(/\bClient\s+Client\s+Support\b/gi, 'Client Support')
      .replace(/\bEquipment\s+Equipment\b(?!\s+Maintenance)/gi, 'Equipment')
      .replace(/\bClient\s+Client\b(?!\s+Support)/gi, 'Client');
    
    let changed = newPlaceholder !== placeholder;
    
    ignitr_brand.brandConfig.replacements.forEach(replacement => {
      const beforeReplace = newPlaceholder;
      
      // Skip if replacement would create duplicates (same logic as text nodes)
      if (replacement.to === "Equipment Maintenance" && /\bEquipment\s+Maintenance\b/i.test(newPlaceholder)) {
        return;
      }
      if (replacement.to === "Client Support" && /\bClient\s+Support\b/i.test(newPlaceholder)) {
        return;
      }
      
      newPlaceholder = newPlaceholder.replace(replacement.from, replacement.to);
      if (beforeReplace !== newPlaceholder) {
        changed = true;
      }
    });
    
    // Final cleanup pass
    const finalPlaceholder = newPlaceholder
      .replace(/\bEquipment\s+Equipment\s+Maintenance\b/gi, 'Equipment Maintenance')
      .replace(/\bClient\s+Client\s+Support\b/gi, 'Client Support')
      .replace(/\bEquipment\s+Equipment\b(?!\s+Maintenance)/gi, 'Equipment')
      .replace(/\bClient\s+Client\b(?!\s+Support)/gi, 'Client');
    
    if (finalPlaceholder !== newPlaceholder) {
      newPlaceholder = finalPlaceholder;
      changed = true;
    }
    
    if (changed && newPlaceholder !== placeholder) {
      el.setAttribute('placeholder', newPlaceholder);
    }
    el.setAttribute('data-ignitr-processed', 'true');
  });
};

// Run on first load
document.addEventListener("DOMContentLoaded", () => {
  ignitr_brand.hideBrowseApps();
  ignitr_brand.hideBrandingFooters();
  ignitr_brand.replaceLabels();
  
  // Also run after a short delay to catch dynamically loaded content
  setTimeout(() => {
    ignitr_brand.hideBrandingFooters();
    ignitr_brand.replaceLabels();
  }, 1000);
});

// And on every Desk route change
if (frappe.router) {
  frappe.router.on("change", () => {
    ignitr_brand.hideBrowseApps();
    ignitr_brand.hideBrandingFooters();
    ignitr_brand.replaceLabels();
  });
}

// Watch for dynamically added content (debounced to prevent excessive calls)
if (window.MutationObserver) {
  let replaceTimeout;
  const observer = new MutationObserver((mutations) => {
    // Only process if there are actual text node additions
    const hasTextNodes = mutations.some(mutation => {
      return Array.from(mutation.addedNodes).some(node => 
        node.nodeType === Node.TEXT_NODE || 
        (node.nodeType === Node.ELEMENT_NODE && node.textContent)
      );
    });
    
    if (!hasTextNodes) {
      return;
    }
    
    // Debounce to prevent excessive calls
    clearTimeout(replaceTimeout);
    replaceTimeout = setTimeout(() => {
      ignitr_brand.hideBrandingFooters();
      ignitr_brand.replaceLabels();
    }, 300);
  });
  
  observer.observe(document.body, {
    childList: true,
    subtree: true,
    characterData: false // Don't watch text changes to avoid loops
  });
}
