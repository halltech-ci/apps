# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_sale_overview(self):
        return self.env.ref('sale.sale_overview_report').report_action(self)
    
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    line_item = fields.Char(string='Item', default='A')
    
    
    
