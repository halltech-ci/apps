# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    
    
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    line_item = fields.Char(string='Item')
    
    
    
