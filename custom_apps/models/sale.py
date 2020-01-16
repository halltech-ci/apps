# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

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
    
    project_id = fields.Many2one("project.project", "Project", ondelete= "set null")
    purchase_order_subject = fields.Text("Objet : ")
    signed_user = fields.Many2one("res.users", string="Signed In User", readonly=True, default= lambda self: self.env.uid)
    sale_order_recipient = fields.Char("Destinataire")
    sale_order_type = fields.Selection(_SALE_ORDER_DOMAINE, string="Domaine",
                                 required=True, index=True, default='fm')
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
