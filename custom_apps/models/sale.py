# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
# class custom_apps(models.Model):
#     _name = 'custom_apps.custom_apps'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

_SALE_ORDER_DOMAINE = [('fm', 'FABRICATION MECANIQUE'),
                          ('cm', 'CONSTRUCTION METALLIQUE'),
                          ('gc', 'GENIE CIVILE'),
                          ('ct', 'CHAUDRONNERIE TUYAUTERIE'),
                          ('em', 'ELECTROMECANIQUE'),
                          ('bt', 'BATIMENT'),
                          ('ra', 'RECTIFICATION AUTOMOBILE'),
                          ('mi', 'MAINTENANCE INDUSTRIELLE'),
                          ('me', 'MAINTENANCE ELECTROMECANIQUE'),
                          ('mm', 'MAINTENANCE MECANIQUE'),
                          ('cu', 'CONSTRUCTION USINE'),
                          ('ep', 'ETUDES DE PROJET')
    ]

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    '''
    @api.depends('order_line.price_total', 'discount_rate', 'tax_id.amount')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = discount_amount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal 
            discount_amount = amount_untaxed * order.discount_rate/100#montant de la remise
            amount_with_discount = amount_untaxed - discount_amount #le montant apres remise
            amount_tax = amount_with_discount * order.tax_id.amount/100#le montant de la tva
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_tax + amount_with_discount,
                'discount_amount': discount_amount,
                'amount_with_discount': amount_with_discount
            })
    '''
    
    project_id = fields.Many2one("project.project", "Project", ondelete= "cascade")
    project_code = fields.Char("Code Projet", related='project_id.project_code')
    description = fields.Text("Description : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    sale_order_recipient = fields.Char("Destinataire")
    sale_order_type = fields.Selection(_SALE_ORDER_DOMAINE, string="Domaine",
                                 required=True, index=True, default='fm')
    discount_rate = fields.Float(string='Discount (%)', digits=dp.get_precision('Discount'), default=0.0)
    #amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    #discount_amount = fields.Monetary(string='Discount Amount', store=True, readonly=True, compute='_amount_all', track_visibility='always')
    #amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    tax_id = fields.Many2one('account.tax', string='Taxes', default=lambda self:self.env['account.tax'].search([('type_tax_use', '=', 'sale')], limit=1))
    #amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    #amount_with_discount = fields.Monetary(string='Amount with discount', store=True, readonly=True, compute='_amount_all')
    #Override create methode to add multiple sequencec
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if vals.get('sale_order_type', 'fm'):
                domaine_code = vals.get('sale_order_type')
                next_code = '{0}.{1}.{2}'.format('sale',domaine_code, 'sequence')
                if 'company_id' in vals:
                    vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(next_code) or _('New')
                else:
                    vals['name'] = self.env['ir.sequence'].next_by_code(next_code) or _('New')

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist and partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"
    
    
    tax_id = fields.Many2one('account.tax', string='Taxes', related="order_id.tax_id")

    #sale order disable inventory check
    @api.onchange('product_uom_qty', 'product_uom')
    def _onchange_product_id_check_availability(self):
        return {}
