# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequestAllocation(models.Model):
    _inherit = "purchase.request.allocation"
    
    project = fields.Many2one("project.project", related="purchase_request_line_id.project")
    project_code = fields.Char(related="project.code")