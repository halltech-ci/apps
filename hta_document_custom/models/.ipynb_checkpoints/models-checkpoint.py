# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DocumentCustom(models.Model):
    _inherit = "documents.document"

	
    @api.constrains('name')
    def _check_unique_document_name(self):
	
        document_ids = self.search([]) - self
	
        value = [ x.name.lower() for x in document_ids ]
	
        if self.name and self.name.lower() in value:
            raise ValidationError(_("Le document existe"))
	
        return True

