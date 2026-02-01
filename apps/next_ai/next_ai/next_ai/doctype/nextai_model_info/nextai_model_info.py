# Copyright (c) 2025, antonykumar15898@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class NextAIModelInfo(Document):
	def on_update(self):
		from next_ai.ai import _clear_nextai_caches
		_clear_nextai_caches()

	def on_trash(self):
		from next_ai.ai import _clear_nextai_caches
		_clear_nextai_caches()
