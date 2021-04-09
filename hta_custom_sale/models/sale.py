# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


_SALE_ORDER_DOMAINE = [('fm', 'FABRICATION MECANIQUE'),
                          ('cm', 'CONSTRUCTION METALLIQUE'),
                          ('gcb', 'GENIE CIVILE ET BATIMENT'),
                          ('fe', 'FOURNITURE EQUIPEMENTS'),
                          ('mi', 'MAINTENANCE INDUSTRIELLE'),
                          ('ec', 'ETUDE ET CONSULTANCE'),
                          ('', '-------------------------'),
                          ('erp', 'ERP'),
                          ('rit', 'RESEAUX, INFORMATIQUE ET TELECOMS'),
                          ('sel', 'SECURITE ELECTRONIQUE'),
                          ('gtp', 'GESTION DE TEMPS')
    ]

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    project_id = fields.Many2one("project.project", "Project", ondelete= "cascade")
    project_code = fields.Char("Code Projet", related='project_id.code')
    description = fields.Text("Description : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    sale_order_recipient = fields.Char("Destinataire")
    sale_order_type = fields.Selection(_SALE_ORDER_DOMAINE, string="Domaine", required=True, index=True, default='fm')
    amount_total_no_tax = fields.Monetary(string='Total HT', store=True, readonly=True, compute='_amount_total_no_tax', tracking=4)
    remise_total = fields.Monetary(string='Remise', store=True, readonly=True, compute='_amount_discount_no', tracking=4)
    sale_margin = fields.Float(string='Coef. Majoration (%)', default=25)
    sale_discuss_margin = fields.Float(string='Disc Margin (%)', default=0.0)
    
    @api.depends('order_line.line_subtotal')
    def _amount_total_no_tax(self):
        for order in self:
            amount_no_tax = 0.0
            for line in order.order_line:
                amount_no_tax += line.line_subtotal
            order.update({
                'amount_total_no_tax': amount_no_tax
            })
    
    @api.depends('amount_total_no_tax')
    def _amount_discount_no(self):
        for order in self:
            order.remise_total = order.amount_total_no_tax - order.amount_untaxed
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            domaine_code = vals.get('sale_order_type')
            next_code = '{0}.{1}.{2}'.format('sale', domaine_code, 'sequence')
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            if 'company_id' in vals:
                #if self.company_id.name == 'CONCEPTOR INDUSTRY':
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    next_code, sequence_date=seq_date) or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code(next_code, sequence_date=seq_date) or _('New')

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
    _inherit = 'sale.order.line'
    
    product_code = fields.Char(related='product_id.default_code', string="Code")
    product_cost = fields.Float(string="Cost", digits='Product Price',)
    line_subtotal = fields.Monetary(compute='_compute_line_subtotal', string='Prix Total', readonly=True, store=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price', default=0.0,
        compute='_compute_price_unit',
        store=True,
    )
    line_margin = fields.Float(compute="_compute_line_margin", store=True, readonly=False,)
    line_discuss_margin = fields.Float(compute="_compute_line_margin", store=True, readonly=False,)
    
    @api.depends("order_id", "order_id.sale_margin", "order_id.sale_discuss_margin")
    def _compute_line_margin(self):
        if hasattr(super(), "_compute_line_margin"):
            super()._compute_line_margin()
        for line in self:
            line.line_margin = line.order_id.sale_margin
            line.line_discuss_margin = line.order_id.sale_discuss_margin
    
    @api.depends('product_uom_qty', 'price_unit')
    def _compute_line_subtotal(self):
        for line in self:
            line.line_subtotal = line.product_uom_qty * line.price_unit
    
    @api.depends('line_margin', 'product_cost')
    def _compute_price_unit(self):
        for line in self:
            line.price_unit += line.product_cost * line.line_margin/100
        
    @api.model
    def create(self, vals):
        """Apply sale margin for sale order lines which are not created
        from sale order form view.
        """
        if "line_margin" not in vals and "order_id" in vals:
            sale_order = self.env["sale.order"].browse(vals["order_id"])
            if sale_order.sale_margin:
                vals["line_margin"] = sale_order.sale_margin
        return super().create(vals)