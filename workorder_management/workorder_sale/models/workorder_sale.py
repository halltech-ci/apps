# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class WorkorderSale(models.Model):
    _name = 'workorder.sale'
    _description = "Create sale order from workorder"
    
    
    name = fields.Char()
    code = fields.Char()
    line_ids = fields.One2many('workorder.line', 'workorder_id')
    company_id = fields.Many2one('res.company', string='Company', required=True, index=True, readonly=True, default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string='Currency', readonly=True, default=lambda self: self.env.company.currency_id)
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_amount_total', tracking=4, default=10)
    workorder_sale_id = fields.Many2one("sale.workorder.sale")
    is_sale = fields.Boolean(compute='_compute_is_sale')
    
    
    @api.depends('workorder_sale_id')
    def _compute_is_sale(self):
        for rec in self:
            if rec.workorder_sale_id:
                rec.is_sale = True
            else: 
                rec.is_sale = False
    
    @api.depends('line_ids.price_subtotal')
    def _compute_amount_total(self):
        for order in self:
            amount = 0
            for line in order.line_ids:
                amount += line.price_subtotal
            order.update({'amount_total': amount,})
            
    @api.model
    def create(self, vals):
        request = super(WorkorderSale, self).create(vals)
        return request
    
    def write(self, vals):
        res = super(WorkorderSale, self).write(vals)
        return res
    
    def unlink(self):
        if any(self.filtered(lambda workorder: workorder.is_sale == True)):
            raise UserError(_('Vous ne pouvez pas supprimer une oeuvre déja utilisé !'))        
        return super(WorkorderSale, self).unlink()
    
class WorkorderLine(models.Model):
    _name = "workorder.line"
    _description = "workorder sale line"
    
    name = fields.Char(string='Description',)
    product_id = fields.Many2one('product.product', string='Product')
    product_template_id = fields.Many2one('product.template', string='Product Template', related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])
    product_uom_qty = fields.Float(string='Quantity', digits='Product Unit of Measure', required=True, default=1.0)
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]", ondelete="restrict")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    currency_id = fields.Many2one(related='workorder_id.currency_id', depends=['company_id.currency_id'], store=True, string='Currency')
    company_id = fields.Many2one(related='workorder_id.company_id', string='Company', store=True, index=True)
    workorder_id = fields.Many2one('workorder.sale', string="Sale workorder", ondelete="cascade", index=True, copy=False)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0, compute='_compute_price_unit', store=True)
    price_tax = fields.Float(string='Total Tax', readonly=True, store=True)
    price_subtotal = fields.Monetary(string='Subtotal', store=True, compute="_compute_subtotal")#egale prix_unitaire * quantite
    price_total = fields.Monetary( string='Total', readonly=True, store=True)#prix total
    discount = fields.Float(string='Remise (%)', digits='Discount', default=0.0)#remise
    product_cost = fields.Float('Cost', required=True, digits='Product Price', default=0.0,)
    line_margin = fields.Float(string="Marge", default=0.0)
    
    
    @api.depends('price_unit', 'product_uom_qty')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.price_unit * line.product_uom_qty
    
    @api.depends('product_cost', 'line_margin', 'product_id.standard_price')
    def _compute_price_unit(self):
        for line in self:
            if line.product_cost != 0:
                line.price_unit = line.product_cost * (1 + line.line_margin/100)
            else:
                line.price_unit = line.product_id.standard_price
                
    
    