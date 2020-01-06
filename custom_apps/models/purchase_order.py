# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    proforma_invoice = fields.Char(string="N° Devis Fournisseur :", store=True)
    total_amount_letter = fields.Text(string="Montant total en lettre:")
    project_id = fields.Many2one("project.project", "Project", ondelete="set null")
    sale_order_id = fields.Many2one("sale.order", "Sale Order", ondelete="set null")
    #product_code = fields.Many2one("product.product", "Product Code", related="product_id.default_code")
    

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"
    
    item = fields.Integer(string="Item", store=True)
    date_planned = fields.Datetime(string='Scheduled Date', required=False, index=True)
    product_code = fields.Char(string = "Product Code", 
                               related="product_id.default_code")
    product_name = fields.Char(string="Product Description", 
                           related="product_id.name")
    
    '''
    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        # Reset date, price and quantity since _onchange_quantity will provide default values
        self.date_planned = datetime.today().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        self.price_unit = self.product_qty = 0.0
        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        #Added By Halltech Africa
        self.product_code = self.product_id.code
        result['domain'] = {'product_uom': [('category_id', '=', self.product_id.uom_id.category_id.id)]}

        product_lang = self.product_id.with_context(
            lang=self.partner_id.lang,
            partner_id=self.partner_id.id,
        )
        self.name = product_lang.display_name
        if product_lang.description_purchase:
            self.name += '\n' + product_lang.description_purchase

        fpos = self.order_id.fiscal_position_id
        if self.env.uid == SUPERUSER_ID:
            company_id = self.env.user.company_id.id
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id.filtered(lambda r: r.company_id.id == company_id))
        else:
            self.taxes_id = fpos.map_tax(self.product_id.supplier_taxes_id)

        self._suggest_quantity()
        self._onchange_quantity()

        return result
    '''
