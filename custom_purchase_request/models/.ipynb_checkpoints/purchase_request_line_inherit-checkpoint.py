# -*- coding: utf-8 -*-

from odoo import models, fields, api


class custom_purchase_request(models.Model):
    _inherit = 'purchase.request.line'
   
    
    @api.onchange("product_id")
    def onchange_product_id(self):
        if self.product_id:
            name = self.product_id.name
            if self.product_id.code:
                name = "{} ({})".format(self.product_id.product_tmpl_id.name, name)
            if self.product_id.description_purchase:
                name += "\n" + self.product_id.description_purchase
            self.product_uom_id = self.product_id.uom_id.id
            self.product_qty = 1
            self.name = name