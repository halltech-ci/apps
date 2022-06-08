# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleWorkorderSale(models.Model):
    _name = "sale.workorder.sale"
    _description = "Use this class to make workorder sale"
    
    name = fields.Char(string='Reference', default='/', required=True, index=True, copy=False, readonly=True)
    workorder_line_ids = fields.One2many('workorder.sale', "workorder_sale_id", string='Workorder line')
    parter_id = fields.Many2one('res.partner', string='Partner')
    state = fields.Selection([('draft', 'Quotation'),
                            ('sent', 'Quotation Sent'),
                            ('sent', 'Quotation Sent'),
                            ('sale', 'Sales Order'),
                            ('done', 'Locked'),
                            ('cancel', 'Cancelled'),], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    