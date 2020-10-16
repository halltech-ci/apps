# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WizardProfitLoss(models.TransientModel):
    _name = "wizard.profit.loss"
    _description = "Default profit loss wizard"
    #_inherit = 'account.report'
    
    company_id = fields.Many2one('res.company', string='Company', readonly=True, default=lambda self: self.env.user.company_id)
    #journal_ids = fields.Many2many('account.journal', string='Journals', required=True, default=lambda self: self.env['account.journal'].search([]))
    #obtenir les lignes comptabilise ou pas
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    analytic_ids = fields.Many2many('account.analytic.account','pl_analytic_rel' ,string="Analytic account")
    start_date = fields.Date(string='Start Date', default=fields.Date.today())
    end_date = fields.Date(string='End Date', default=fields.Date.today())
    
    def check_date_range(self):
        if self.end_date < self.start_date:
            raise ValidationError(_('Enter proper date range'))
    
    @api.multi
    def view_report(self):
        self.check_date_range()
        datas = {'form':
            {
                'company_id': self.company_id.id,
                'analytic_ids': [y.id for y in self.analytic_ids],
                #'location_id': self.location_id and self.location_id.id or False,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'id': self.id,
                'target_move': self.target_move,
            },
        }
        return self.env.ref('hta_custom_report.action_hta_custom_report').report_action(self, data=datas)
    