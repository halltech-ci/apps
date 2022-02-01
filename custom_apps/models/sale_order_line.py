# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    price_subtotal = fields.Monetary(compute='_compute_subtotal', string='Subtotal', readonly=True, store=True)
    price_tax = fields.Float(compute='_compute_subtotal', string='Total Tax', readonly=True, store=True)
    price_total = fields.Monetary(compute='_compute_subtotal', string='Total', readonly=True, store=True)

    @api.depends('price_unit','product_uom_qty','sde_price_unite','discount', 'price_unit', 'tax_id')
    def _compute_subtotal(self):
        for record in self:
            if record.sde_price_unite > 0:
                price = record.price_unit * (1 - (record.discount or 0.0) / 100.0)
                taxes = record.tax_id.compute_all(price, record.order_id.currency_id, record.secondary_uom_qty, product=record.product_id, partner=record.order_id.partner_shipping_id)
                record.update({
                        'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                        'price_total': taxes['total_included'],
                        'price_subtotal': taxes['total_excluded'],
                    })
            
            else:
                for line in self:
                    price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                    taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_shipping_id)
                    line.update({
                        'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                        'price_total': taxes['total_included'],
                        'price_subtotal': taxes['total_excluded'],
                    })
                    if self.env.context.get('import_file', False) and not self.env.user.user_has_groups('account.group_account_manager'):
                        line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])

                
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    sde_price_unite = fields.Float(string="Sde Price Unite", store=True, compute='_compute_sde_price')
    
    @api.depends('price_unit','secondary_uom_qty','secondary_uom_id')
    def _compute_sde_price(self):
        for record in self:
            if record.secondary_uom_id:
                record.sde_price_unite = (record.price_unit * record.secondary_uom_qty)
            else:
                record.sde_price_unite = 0
                
