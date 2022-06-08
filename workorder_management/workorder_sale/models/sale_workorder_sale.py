# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleWorkorderSale(models.Model):
    _name = "sale.workorder.sale"
    _description = "Use this class to make workorder sale"
    
    name = fields.Char(string='Reference', default='/', required=True, index=True, copy=False, readonly=True)
    #workorder_line_ids = fields.One2many('workorder.sale', "workorder_sale_id", string='Workorder line')
    sale_workorder_ids = fields.One2many('sale.workorder.sale.line', 'sale_workorder_id',string='Work order line')
    parter_id = fields.Many2one('res.partner', string='Partner')
    state = fields.Selection([('draft', 'Quotation'),
                            ('sent', 'Quotation Sent'),
                            ('sent', 'Quotation Sent'),
                            ('sale', 'Sales Order'),
                            ('done', 'Locked'),
                            ('cancel', 'Cancelled'),], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    
    
    
    
    
class SaleWorkorderSaleLine(models.Model):
    _name = 'sale.workorder.sale.line'
    _description = "Line to use to sale work"
    
    name = fields.Char()
    workorder_id = fields.Many2one('workorder.sale')
    sale_workorder_id = fields.Many2one('sale.workorder.sale')
    quantity = fields.Float(string='Qty')
    currency_id = fields.Many2one(related='workorder_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')
    company_id = fields.Many2one(related='workorder_id.company_id', string='Company', store=True, index=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, compute='_compute_price_unit', store=True)
    price_tax = fields.Float(string='Total Tax', readonly=True, store=True)
    price_subtotal = fields.Monetary(string='Subtotal', store=True, compute="_compute_subtotal")#egale prix_unitaire * quantite
    price_total = fields.Monetary( string='Total', readonly=True, store=True)#prix total
    discount = fields.Float(string='Remise (%)', digits='Discount', default=0.0)#remise
    product_cost = fields.Float('Cost', required=True, digits='Product Price', default=0.0,)
    line_margin = fields.Float(string="Marge", default=0.0)
    
    
    @api.depends('price_unit', 'quantity')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.quantity
    
    @api.depends('product_cost', 'line_margin', 'workorder_id.amount_total')
    def _compute_price_unit(self):
        for line in self:
            if line.product_cost != 0:
                line.price_unit = line.product_cost * (1 + line.line_margin/100)
            else:
                line.price_unit = line.workorder_id.amount_total
    
    
    