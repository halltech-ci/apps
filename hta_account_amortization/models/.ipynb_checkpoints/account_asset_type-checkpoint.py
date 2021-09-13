# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime
import calendar

class hta_account_amortization(models.Model):
    _name = 'hta.account_asset.type'
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin','portal.mixin']
    _description = 'Account Asset Type'

    
    def _default_currency_id(self):
        company_id = self.env.context.get('force_company') or self.env.context.get('company_id') or self.env.company.id
        return self.env['res.company'].browse(company_id).currency_id
    
            
    name = fields.Char()
    number_percentage = fields.Integer()
    asset_ids = fields.One2many('account.asset','type_asset_ids', string='Immobilisation')
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', required=True,default=_default_currency_id)



            
class hta_account_amortization(models.Model):
    _inherit = "account.asset"
    
    @api.depends('depreciation_move_ids')
    def _amount_for_asset(self):
        for rec in self:
            amount_exercice = amount_exercice = 0.0
            totals = totals = 0.0
            valeur_residuelle = valeur_residuelle = 0.04
            date_now = datetime.now().date()
            ending_days_month = date_now.replace(day=calendar.monthrange(date_now.year, date_now.month)[1])
            first_day_of_current_year = datetime.now().date().replace(month=1, day=1)
            ending_day_of_current_year = datetime.now().date().replace(month=12, day=31)
            if rec.method_period == "12":
                for line in rec.depreciation_move_ids:
                    if first_day_of_current_year <= line.date and line.date >= ending_day_of_current_year:
                        amount_exercice = line.amount_total
                        totals = line.asset_depreciated_value
                        valeur_residuelle = line.asset_remaining_value
            else:
                for line in rec.depreciation_move_ids:
                    if date_now <= line.date and line.date >= ending_days_month:
                        amount_exercice = line.amount_total
                        totals = line.asset_depreciated_value
                        valeur_residuelle = line.asset_remaining_value
                
            currency = rec.currency_id or self.env.company.currency_id
            
            rec.update({
                'amount_exercice': currency.round(amount_exercice),
                'totals': currency.round(totals),
                'valeur_residuelle': currency.round(valeur_residuelle),
            })
    
    amount_exercice = fields.Monetary(string='Total Valeur Exercice', store=True, readonly=True, compute='_amount_for_asset',states={'draft': [('readonly', False)]})
    totals = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_for_asset',states={'draft': [('readonly', False)]})
    valeur_residuelle = fields.Monetary(string='Total Residuelle', store=True, readonly=True, compute='_amount_for_asset',states={'draft': [('readonly', False)]})
    
    type_asset_ids = fields.Many2one(comodel_name='hta.account_asset.type', index=True)
    method_number = fields.Integer(string='Number of Depreciations', readonly=True, states={'draft': [('readonly', False)], 'model': [('readonly', False)]}, default=5, compute='_compute_method_number',help="The number of depreciations needed to depreciate your asset")
    
            
    @api.depends('type_asset_ids','type_asset_ids.number_percentage')
    def _compute_method_number(self):
        for record in self:
            record.method_number = record.type_asset_ids.number_percentage



