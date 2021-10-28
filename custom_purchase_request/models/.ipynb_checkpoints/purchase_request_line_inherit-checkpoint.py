# -*- coding: utf-8 -*-

from odoo import models, fields, api


class custom_purchase_request(models.Model):
    _inherit = 'purchase.request.line'
   
    
    
    @api.onchange("product_id")
    def onchange_product_id(self):
        for rec in self:
            if rec.product_id:
                name = rec.product_id.name
                if rec.product_id.code:
                    name = "{} (".format(rec.product_id.product_tmpl_id.name, name)
                    for no_variant_attribute_value in rec.product_id.product_template_attribute_value_ids:
                        name += "{}".format(no_variant_attribute_value.name + ', ')
                    name += ")"
                if rec.product_id.description_purchase:
                    name += "\n" + rec.product_id.description_purchase
                rec.product_uom_id = rec.product_id.uom_id.id
                rec.product_qty = 1
                rec.name = name