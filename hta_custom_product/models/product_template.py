# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"
    #Make default_code field mandatory
    def _get_sale_uom_id(self):
        return self.env["uom.uom"].search([], limit=1, order='id').id
    
    type = fields.Selection(default='service')
    uom_so_id = fields.Many2one('uom.uom', 'Sale Unit of Measure', default=_get_sale_uom_id, 
        help="Default Unit of Measure used for sale orders. It must be in the same category than the default unit of measure.")