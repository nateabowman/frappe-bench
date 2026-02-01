import frappe


def execute():
	frappe.reload_doc("website", "doctype", "web_page_view", force=True)
	site_url = frappe.utils.get_site_url(frappe.local.site)
	frappe.db.sql(
		"""UPDATE `tabWeb Page View` SET is_unique=1 WHERE referrer LIKE %s""",
		(f"%{site_url}%",),
	)
