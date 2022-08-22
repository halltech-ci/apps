# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'
    
    purchase_type = fields.Selection(selection_add=[('service', 'Prestation de service')])