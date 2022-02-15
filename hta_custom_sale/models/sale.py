# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from num2words import num2words
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

_SALE_ORDER_DOMAINE = [('fm', ''),
                          ('cmgc', 'CONSTRUCTION METALLIQUE ET GENIE CIVIL'),
                          ('fmfe', "FABRICATION MECANIQUE ET FOURNITURE D'EQUIPEMENTS"),
                          ('mips', 'MAINTENANCE INDUSTRIELLE ET PRESTATION DE SERVICES'),
                          ('bec', "BUREAU D'ETUDE ET CONSULTANCE"),
                          ('', '-------------------------'),
                          ('erp', 'ERP'),
                          ('rit', 'RESEAUX, INFORMATIQUE ET TELECOMS'),
                          ('sel', 'SECURITE ELECTRONIQUE'),
                          ('gtp', 'GESTION DE TEMPS')
    ]

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    @api.model
    def _default_note(self):
        return self.env['ir.config_parameter'].sudo().get_param('account.use_invoice_terms') and self.env.company.invoice_terms or ''
    #num2words convert number to word
    def _num_to_words(self, num):
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()
        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        num_to_word = _num2words(num, lang=lang.iso_code)
        return num_to_word
        
    #sequence_id = fields.Many2one('sale.order.type', string="Sequence", required=True, ondelete='restrict', copy=True, default=lambda so: so._default_type_id(), )
    date_order = fields.Datetime(readonly=False)
    is_proforma = fields.Boolean('Proformat', default=False)
    description = fields.Text("Description : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    sale_order_recipient = fields.Char("Destinataire")
    sale_order_type = fields.Selection(_SALE_ORDER_DOMAINE, string="Domaine", required=True, index=True, default='fm')
    amount_total_no_tax = fields.Monetary(string='Total HT', store=True, readonly=True, compute='_amount_total_no_tax', tracking=4)
    remise_total = fields.Monetary(string='Remise', store=True, readonly=True, compute='_amount_discount_no', tracking=4)
    sale_margin = fields.Float(string='Coef. Majoration (%)', default=25)
    sale_discuss_margin = fields.Float(string='Disc Margin (%)', default=0.0, copy=True)
    amount_to_word = fields.Char(string="Amount In Words:", compute='_compute_amount_to_word')        
    note = fields.Text('Termes et conditions', default=_default_note, required=True)
    total_cost = fields.Monetary(string="Cout Total", compute='_compute_total_cost')
    total_margin_amount = fields.Monetary(string="Marge Brut", compute="_compute_total_margin_amount")
    
    @api.depends('order_line.product_cost', )
    def _compute_total_cost(self): 
        for rec in self:
            total_cost = 0
            for line in rec.order_line:
                total_cost += line.product_cost
            rec.total_cost = total_cost
        
    
    @api.depends('total_cost', 'amount_total_no_tax')
    def _compute_total_margin_amount(self):
        for rec in self:
            rec.total_margin_amount = rec.amount_total_no_tax - rec.total_cost

    @api.onchange('sale_margin')
    def onchange_sale_margine(self):
        for line in self.order_line:
            line.line_margin = self.sale_margin            
            
    def _compute_amount_to_word(self):
        for rec in self:
            rec.amount_to_word = str(self._num_to_words(rec.amount_total)).upper()
    
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
            next_code = "sale.order"
            domaine_code = vals.get('sale_order_type')
            if domaine_code != "fm":
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
    
    #product_code = fields.Char(related='product_id.default_code', string="Code")
    product_cost = fields.Float(string="Cost", digits='Product Price', copy=True)
    line_subtotal = fields.Monetary(compute='_compute_line_subtotal', string='Prix Total', readonly=True, store=True, copy=True)
    price_unit = fields.Float('Unit Price', required=True, digits='Product Price',
        compute='_compute_price_unit',
        store=True,
        copy=True
    )
    line_margin = fields.Float(compute="_compute_line_margin", store=True, readonly=False, copy=True)
    line_discuss_margin = fields.Float(compute="_compute_line_margin", store=True, readonly=False, copy=True)
    
    @api.onchange('product_cost')
    def _onchange_product_cost(self):
        self.price_unit = self.product_cost * (1 + self.line_margin/100 + self.line_discuss_margin/100)
        self.line_subtotal = self.product_uom_qty * self.price_unit
        
    @api.onchange('product_uom_qty')
    def _onchange_product_cost(self):
        self.price_unit = self.product_cost * (1 + self.line_margin/100 + self.line_discuss_margin/100)
        self.line_subtotal = self.product_uom_qty * self.price_unit

    
    """@api.onchange('product_uom_qty')
    def _onchange_product_qty(self):
        if self.product_cost > 0 :
            self.price_unit = self.product_cost * (1 + self.line_margin/100 + self.line_discuss_margin/100)
            self.line_subtotal = self.product_uom_qty * self.price_unit
    """
    @api.onchange('line_margin')
    def _onchange_line_margin(self):
        if self.product_cost > 0 :
            self.price_unit = self.product_cost * (1 + self.line_margin/100 + self.line_discuss_margin/100)
            self.line_subtotal = self.product_uom_qty * self.price_unit
    
    @api.depends("order_id", "order_id.sale_margin", "order_id.sale_discuss_margin")
    def _compute_line_margin(self):
        if hasattr(super(), "_compute_line_margin"):
            super()._compute_line_margin()
        for line in self:
            #line_margin = line.order_id.sale_margin
            #line_discuss_margin = line.order_id.sale_discuss_margin
            if not line.line_margin:
                line.line_margin = line.order_id.sale_margin
            if not line.line_discuss_margin:
                line.line_discuss_margin = line.order_id.sale_discuss_margin
    
    @api.depends('product_uom_qty', 'price_unit')
    def _compute_line_subtotal(self):
        for line in self:
            line.line_subtotal = line.product_uom_qty * line.price_unit
    
    @api.depends('line_margin', 'product_cost')
    def _compute_price_unit(self):
        for line in self:
            if line.product_cost > 0 :
                line.price_unit = line.product_cost * (1 + line.line_margin/100 + line.line_discuss_margin/100)
        
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