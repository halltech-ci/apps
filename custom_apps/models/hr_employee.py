# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit="hr.employee"
    
    hiring_date = fields.Date(string='Hiring Date', required=True, default=fields.Date.today())
    seniority = fields.Integer(string="Seniority", store=True, compute='_compute_seniority')
      
    @api.depends('hiring_date')
    def _compute_seniority(self):
        today = fields.Date.today()
        today_date = fields.Date.from_string(today)
        for rec in self:
            age = today_date - fields.Date.from_string(rec.hiring_date)
            rec.seniority = int(age.days/366)

    
    
    