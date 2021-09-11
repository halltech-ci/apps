# -*- coding: utf-8 -*-

from odoo import models, fields, api


class hta_account_amortization(models.Model):
    _name = 'hta.account_asset.type'
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin','portal.mixin']
    _description = 'Account Asset Type'

    
    def _default_currency_id(self):
        company_id = self.env.context.get('force_company') or self.env.context.get('company_id') or self.env.company.id
        return self.env['res.company'].browse(company_id).currency_id
    
    @api.depends('asset_ids')
    def _amount_all(self):
        for order in self:
            total_valeur_acquisition = total_valeur_acquisition = 0.0
            total_exercice = total_exercice = 0.0
            total_total = total_total = 0.0
            total_valeur_residuelle = total_valeur_residuelle = 0.0
            for line in order.asset_ids:
                line._compute_amount()
                total_valeur_acquisition += line.original_value
                total_exercice += line.amount_exercice
                total_total += line.totals
                total_valeur_residuelle += line.valeur_residuelle
                
            currency = order.currency_id or self.env.company.currency_id
            order.update({
                'total_valeur_acquisition': currency.round(total_valeur_acquisition),
                'total_exercice': currency.round(total_exercice),
                'total_total': currency.round(total_total),
                'total_valeur_residuelle': currency.round(total_valeur_residuelle),
            })
    name = fields.Char()
    number_percentage = fields.Integer()
    asset_ids = fields.One2many('account.asset','type_asset_ids', string='Immobilisation')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,default=_default_currency_id)
    total_valeur_acquisition = fields.Monetary(string='Valeur acquisition', store=True, readonly=True, compute='_amount_all')
    total_exercice = fields.Monetary(string='Valeur Exercice', store=True, readonly=True, compute='_amount_all')
    total_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    total_valeur_residuelle = fields.Monetary(string='Total Residuelle', store=True, readonly=True, compute='_amount_all')



            
class hta_account_amortization(models.Model):
    _inherit = "account.asset"
    
    @api.depends('depreciation_move_ids')
    def _amount_for_asset(self):
        for rec in self:
            amount_exercice = amount_exercice = 0.0
            totals = totals = 0.0
            valeur_residuelle = valeur_residuelle = 0.0
            for line in rec.depreciation_move_ids:
                rec._compute_amount()
                amount_exercice += rec.amount_total
                totals += rec.asset_depreciated_value
                valeur_residuelle += rec.asset_remaining_value
                
            currency = rec.currency_id or self.env.company.currency_id
            
            rec.update({
                'amount_exercice': currency.round(amount_exercice),
                'totals': currency.round(totals),
                'valeur_residuelle': currency.round(valeur_residuelle),
            })
    
    amount_exercice = fields.Monetary(string=' Total Valeur Exercice', store=True, readonly=True, compute='_amount_for_asset')
    totals = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_for_asset')
    valeur_residuelle = fields.Monetary(string='Total Residuelle', store=True, readonly=True, compute='_amount_for_asset')
    
    type_asset_ids = fields.Many2one(comodel_name='hta.account_asset.type', index=True)
    method_number = fields.Integer(string='Number of Depreciations', readonly=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, default=5, compute='_compute_method_number',help="The number of depreciations needed to depreciate your asset")
    
            
    @api.depends('type_asset_ids','type_asset_ids.number_percentage')
    def _compute_method_number(self):
        for record in self:
            record.method_number = record.type_asset_ids.number_percentage



