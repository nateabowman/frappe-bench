// File: ignitr_brand/public/js/hide_integration.js
frappe.provide("ignitr_brand");

ignitr_brand.hideIntegrationTab = () => {
  // Adjust selector if your label differs
  const sel = '.module-card[data-label="Ignitr ERP Integrations"]';
  document.querySelectorAll(sel).forEach(el => el.remove());
};

// Run on initial load
document.addEventListener("DOMContentLoaded", ignitr_brand.hideIntegrationTab);

// And on every desk route change
if (frappe.router) {
  frappe.router.on("change", ignitr_brand.hideIntegrationTab);
}
