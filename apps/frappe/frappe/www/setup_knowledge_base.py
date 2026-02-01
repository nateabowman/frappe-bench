# Copyright (c) 2025, Nexelya LLC and contributors
# Run with: bench --site <your-site> execute frappe.www.setup_knowledge_base.run

import frappe


# Static category links and search for KB landing (safe_exec does not expose frappe.website)
KB_LANDING_HTML = """<div class="kb-landing">
	<nav class="kb-nav">
		<div class="kb-nav-inner container">
			<a class="kb-nav-brand" href="/apps">Nexelya</a>
			<div class="kb-nav-links">
				<a href="/apps">Home / Apps</a>
				<span class="kb-nav-current">Knowledge Base</span>
				<a href="/kb/getting-started">Getting Started</a>
				<a href="/kb/platform-overview">Platform Overview</a>
				<a href="/kb/all">Search all</a>
			</div>
		</div>
	</nav>
	<div class="kb-hero">
		<div class="container">
			<h1 class="kb-hero-title">Knowledge Base</h1>
			<p class="kb-hero-lead">Guides and answers for every part of the Nexelya platform.</p>
		</div>
	</div>
	<div class="container kb-main">
		<section class="kb-search-section" id="search">
			<h2 class="kb-section-title">Search articles</h2>
			<form class="kb-search-form" method="get" action="/kb/all" role="search">
				<div class="input-group">
					<input id="kb-search" name="txt" type="search" class="form-control" placeholder="e.g. invoice, leave, pipeline..." aria-label="Search Knowledge Base" />
					<button type="submit" class="btn btn-primary">Search</button>
				</div>
				<small class="text-muted">Searches across all categories. Or open a category below to search only that section.</small>
			</form>
		</section>
		<section class="kb-categories-section">
			<h2 class="kb-section-title">Browse by category</h2>
			<div class="row kb-category-grid">
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/all"><span class="kb-category-name">All</span><span class="kb-category-desc">Search across all categories</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/getting-started"><span class="kb-category-name">Getting Started</span><span class="kb-category-desc">Log in, apps, navigation, help</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/platform-overview"><span class="kb-category-name">Platform Overview</span><span class="kb-category-desc">Roles, workspaces, integrations</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/nexelya-erp"><span class="kb-category-name">Nexelya ERP</span><span class="kb-category-desc">Accounting, inventory, sales</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/crm"><span class="kb-category-name">CRM</span><span class="kb-category-desc">Leads, deals, pipeline</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/drive"><span class="kb-category-name">Drive</span><span class="kb-category-desc">Files, folders, sharing</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/insights"><span class="kb-category-name">Insights</span><span class="kb-category-desc">Reports, queries, dashboards</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/gameplan"><span class="kb-category-name">Gameplan</span><span class="kb-category-desc">Discussions, collaboration</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/construction"><span class="kb-category-name">Construction</span><span class="kb-category-desc">Projects, job costing, field</span></a></div>
				<div class="col-sm-6 col-lg-4 mb-3"><a class="kb-category-card" href="/kb/hr-workforce"><span class="kb-category-name">HR & Workforce</span><span class="kb-category-desc">Employees, leave, payroll</span></a></div>
			</div>
		</section>
		<footer class="kb-footer">
			<p class="text-muted small mb-0">Can't find what you need? <a href="/kb/getting-started">Start here</a> or contact your administrator for support.</p>
		</footer>
	</div>
</div>"""

# CSS for KB landing: layout, nav, hero, cards, margins
KB_LANDING_CSS = """
.kb-landing { min-height: 100vh; background: var(--gray-50, #f8f9fa); }
.kb-nav { background: var(--gray-100, #f1f3f5); border-bottom: 1px solid var(--gray-200, #dee2e6); padding: 0.75rem 0; }
.kb-nav-inner { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; }
.kb-nav-brand { font-weight: 700; font-size: 1.25rem; color: var(--primary, #2490ef); text-decoration: none; }
.kb-nav-brand:hover { color: var(--primary, #2490ef); text-decoration: underline; }
.kb-nav-links { display: flex; flex-wrap: wrap; align-items: center; gap: 1rem; margin-left: auto; }
.kb-nav-links a { color: var(--gray-700, #495057); text-decoration: none; font-size: 0.9375rem; }
.kb-nav-links a:hover { color: var(--primary, #2490ef); text-decoration: underline; }
.kb-nav-current { color: var(--gray-600, #868e96); font-size: 0.9375rem; font-weight: 500; }
.kb-hero { background: var(--white, #fff); border-bottom: 1px solid var(--gray-200, #dee2e6); padding: 2.5rem 0; text-align: center; }
.kb-hero-title { font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: var(--gray-900, #212529); }
.kb-hero-lead { font-size: 1.125rem; color: var(--gray-600, #868e96); margin: 0; }
.kb-main { max-width: 900px; margin: 0 auto; padding: 2rem 1rem 3rem; }
.kb-search-section { background: var(--white, #fff); border-radius: 0.5rem; padding: 1.5rem; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }
.kb-section-title { font-size: 1.25rem; font-weight: 600; margin-bottom: 1rem; color: var(--gray-900, #212529); }
.kb-search-form .input-group { max-width: 28rem; margin-bottom: 0.5rem; }
.kb-categories-section { margin-bottom: 2rem; }
.kb-category-grid { margin: 0 -0.5rem; }
.kb-category-card { display: block; background: var(--white, #fff); border: 1px solid var(--gray-200, #dee2e6); border-radius: 0.5rem; padding: 1.25rem; text-decoration: none; color: inherit; transition: border-color 0.15s, box-shadow 0.15s; }
.kb-category-card:hover { border-color: var(--primary, #2490ef); box-shadow: 0 4px 12px rgba(0,0,0,0.08); color: inherit; text-decoration: none; }
.kb-category-name { display: block; font-weight: 600; color: var(--gray-900, #212529); margin-bottom: 0.25rem; }
.kb-category-desc { display: block; font-size: 0.875rem; color: var(--gray-600, #868e96); }
.kb-footer { padding-top: 1.5rem; border-top: 1px solid var(--gray-200, #dee2e6); text-align: center; }
@media (max-width: 576px) { .kb-nav-links { margin-left: 0; } .kb-hero-title { font-size: 1.5rem; } }
"""


def fix_kb_web_page_context_script():
	"""Remove context_script from KB Web Page and set static layout with nav, hero, search, category grid.
	Run with: bench --site <site> execute frappe.www.setup_knowledge_base.fix_kb_web_page_context_script
	"""
	if _update_kb_web_page_layout():
		print("Updated Web Page (removed context_script, set layout with nav, hero, search, category grid).")


def ensure_all_category():
	"""Create Help Category 'All' (route kb/all) if missing, so search-all works."""
	if frappe.db.exists("Help Category", "All"):
		return
	cat = frappe.get_doc(
		{
			"doctype": "Help Category",
			"category_name": "All",
			"category_description": "Search across all categories. Use this to find articles by keyword in any section.",
			"published": 1,
			"route": "kb/all",
		}
	)
	cat.insert()
	frappe.db.commit()
	print("Created Help Category: All (route: kb/all).")


def _update_kb_web_page_layout():
	"""Set KB Web Page main_section_html, css, full_width. Used by fix and update. Returns True if updated."""
	name = frappe.db.get_value("Web Page", {"route": "kb"}, "name")
	if not name:
		print("No Web Page with route 'kb' found.")
		return False
	doc = frappe.get_doc("Web Page", name)
	doc.context_script = None
	doc.main_section_html = KB_LANDING_HTML
	doc.css = KB_LANDING_CSS
	doc.full_width = 0
	doc.save()
	frappe.db.commit()
	return True


def update_kb_landing_html():
	"""Refresh the KB landing page HTML and styles (e.g. after changing KB_LANDING_HTML or KB_LANDING_CSS).
	Run with: bench --site <site> execute frappe.www.setup_knowledge_base.update_kb_landing_html
	"""
	ensure_all_category()
	_update_kb_web_page_layout()
	print("KB landing page HTML and styles updated.")


def run():
	"""Create Knowledge Base Web Page, Help Categories, and initial Help Articles.
	Run with: bench --site <your-site> execute frappe.www.setup_knowledge_base.run
	"""
	create_kb_web_page()
	categories = create_help_categories()
	create_help_articles(categories)
	frappe.db.commit()
	print("Knowledge Base setup complete. Visit /kb on your site.")


def create_kb_web_page():
	if frappe.db.exists("Web Page", {"route": "kb"}):
		print("Web Page with route 'kb' already exists. Skipping.")
		return
	wp = frappe.get_doc(
		{
			"doctype": "Web Page",
			"title": "Knowledge Base",
			"route": "kb",
			"published": 1,
			"content_type": "HTML",
			"main_section_html": KB_LANDING_HTML,
			"css": KB_LANDING_CSS,
			"full_width": 0,
		}
	)
	wp.insert()
	print("Created Web Page: Knowledge Base (route: kb)")


def create_help_categories():
	categories_config = [
		("All", "Search across all categories. Use this to find articles by keyword in any section."),
		("Getting Started", "First steps: logging in, the apps screen, navigation, and finding help."),
		("Platform Overview", "How the Nexelya platform fits together: roles, workspaces, and switching between apps."),
		("Nexelya ERP", "ERP: accounting, inventory, sales, purchasing, and operations."),
		("CRM", "CRM: leads, deals, contacts, and pipeline."),
		("Drive", "Drive: files, folders, sharing, and version history."),
		("Insights", "Insights: reports, queries, and dashboards."),
		("Gameplan", "Gameplan: discussions and collaboration."),
		("Construction", "Construction: projects, job costing, and field operations."),
		("HR & Workforce", "HR and payroll: employees, attendance, leave, and payroll."),
	]
	created = []
	for category_name, description in categories_config:
		if frappe.db.exists("Help Category", category_name):
			print(f"Help Category '{category_name}' already exists. Skipping.")
			created.append(category_name)
			continue
		cat = frappe.get_doc(
			{
				"doctype": "Help Category",
				"category_name": category_name,
				"category_description": description,
				"published": 1,
			}
		)
		cat.insert()
		created.append(category_name)
		print(f"Created Help Category: {category_name}")
	return created


def create_help_articles(categories):
	"""Create Help Articles from kb_article_definitions (50+ per category). Skips existing."""
	from frappe.www.kb_article_definitions import get_articles_by_category

	articles_by_category = get_articles_by_category()
	for category_name in categories:
		articles = articles_by_category.get(category_name, [])
		for item in articles:
			title = item["title"]
			content = item["content"]
			level = item.get("level", "Beginner")
			name = _unique_help_article_name(category_name, title)
			if frappe.db.exists("Help Article", name):
				continue
			if frappe.db.exists("Help Article", {"title": title, "category": category_name}):
				continue
			art = frappe.get_doc(
				{
					"doctype": "Help Article",
					"title": title,
					"category": category_name,
					"content": content,
					"level": level,
					"published": 1,
				}
			)
			art.name = name
			art.flags.name_set = True
			art.insert()
			print(f"  Created Help Article: {title} (in {category_name})")


def add_bulk_articles():
	"""Add all articles from kb_article_definitions. Use on existing sites to expand from 2 to 50+ per category.
	Run with: bench --site <site> execute frappe.www.setup_knowledge_base.add_bulk_articles
	"""
	from frappe.www.kb_article_definitions import get_articles_by_category

	articles_by_category = get_articles_by_category()
	for category_name, articles in articles_by_category.items():
		if not frappe.db.exists("Help Category", category_name):
			print(f"  Skipping unknown category: {category_name}")
			continue
		for item in articles:
			title = item["title"]
			content = item["content"]
			level = item.get("level", "Beginner")
			name = _unique_help_article_name(category_name, title)
			if frappe.db.exists("Help Article", name):
				continue
			if frappe.db.exists("Help Article", {"title": title, "category": category_name}):
				continue
			art = frappe.get_doc(
				{
					"doctype": "Help Article",
					"title": title,
					"category": category_name,
					"content": content,
					"level": level,
					"published": 1,
				}
			)
			art.name = name
			art.flags.name_set = True
			art.insert()
			print(f"  Created Help Article: {title} (in {category_name})")
	frappe.db.commit()
	print("Bulk articles added. Visit /kb on your site.")


def _unique_help_article_name(category_name: str, title: str) -> str:
	"""Return a unique name for Help Article so same title in different categories does not collide."""
	slug_cat = frappe.scrub(category_name).replace("_", "-")
	slug_title = frappe.scrub(title).replace("_", "-")
	name = f"{slug_cat}-{slug_title}"[:140]
	return name
