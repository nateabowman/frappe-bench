# Copyright (c) 2015, Nexelya Technologies Pvt. Ltd. and Contributors
# MIT License. See LICENSE

from frappe.exceptions import ValidationError


class NewsletterAlreadySentError(ValidationError):
	pass


class NoRecipientFoundError(ValidationError):
	pass


class NewsletterNotSavedError(ValidationError):
	pass
