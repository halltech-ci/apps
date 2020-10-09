# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class hta_custom_report(models.Model):
#     _name = 'hta_custom_report.hta_custom_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100


class AccountProfitLoss(models.AbstractModel):
    _name = "account.profit.loss"
    _inherit = "account.report"
    _description = "Default profit loss report"
    
    filter_date = {'date_from': '', 'date_to': '', 'filter': 'this_year'}
    filter_unfold_all = False
    #filter_analytic = None
    
    def _get_filter_journals(self):
        return self.env['account.journal'].search([('company_id', 'in', [self.env.user.company_id.id, False])], order="company_id, name")
    
    