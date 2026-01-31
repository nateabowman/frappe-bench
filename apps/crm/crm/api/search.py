import frappe
from frappe import _


@frappe.whitelist()
def global_search(query: str, limit: int = 10):
	"""
	Perform global search across CRM entities (Leads, Deals, Contacts, Organizations)
	"""
	if not query or len(query.strip()) < 2:
		return []

	search_term = f"%{query.strip()}%"
	results = []

	# Search Leads
	leads = frappe.db.sql(
		"""
		SELECT name, lead_name as title, 'CRM Lead' as doctype
		FROM `tabCRM Lead`
		WHERE (lead_name LIKE %(term)s OR email LIKE %(term)s OR mobile_no LIKE %(term)s)
		AND docstatus != 2
		ORDER BY modified DESC
		LIMIT %(limit)s
		""",
		{"term": search_term, "limit": limit},
		as_dict=True,
	)
	results.extend(leads)

	# Search Deals
	deals = frappe.db.sql(
		"""
		SELECT name, name as title, 'CRM Deal' as doctype
		FROM `tabCRM Deal`
		WHERE name LIKE %(term)s
		AND docstatus != 2
		ORDER BY modified DESC
		LIMIT %(limit)s
		""",
		{"term": search_term, "limit": limit},
		as_dict=True,
	)
	results.extend(deals)

	# Search Contacts
	contacts = frappe.db.sql(
		"""
		SELECT name, CONCAT(IFNULL(first_name, ''), ' ', IFNULL(last_name, '')) as title, 'CRM Contact' as doctype
		FROM `tabCRM Contact`
		WHERE (first_name LIKE %(term)s OR last_name LIKE %(term)s OR email LIKE %(term)s)
		AND docstatus != 2
		ORDER BY modified DESC
		LIMIT %(limit)s
		""",
		{"term": search_term, "limit": limit},
		as_dict=True,
	)
	results.extend(contacts)

	# Search Organizations
	organizations = frappe.db.sql(
		"""
		SELECT name, organization_name as title, 'CRM Organization' as doctype
		FROM `tabCRM Organization`
		WHERE organization_name LIKE %(term)s
		AND docstatus != 2
		ORDER BY modified DESC
		LIMIT %(limit)s
		""",
		{"term": search_term, "limit": limit},
		as_dict=True,
	)
	results.extend(organizations)

	# Remove duplicates and limit total results
	seen = set()
	unique_results = []
	for result in results:
		key = (result.doctype, result.name)
		if key not in seen:
			seen.add(key)
			unique_results.append(result)
			if len(unique_results) >= limit:
				break

	return unique_results

