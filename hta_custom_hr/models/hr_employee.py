# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit="hr.employee"
    
    hiring_date = fields.Date(string='Hiring Start Date', related="contract_id.date_start")
    
    hiring_end = fields.Date(string='End Hiring Date', default=fields.Date.today())
    seniority = fields.Integer(string="Seniority", store=True, compute='_compute_seniority')
    nbre_part = fields.Float(string="Nombre de Part", default=1)
    partner_id = fields.Many2one('res.partner', string="Partner", ondelete="cascade")
    certificate = fields.Selection([
        ('CEPE', 'CEPE'),
        ('BEPC', 'BEPC'),
        ('BAC', 'BAC'),
        ('BAC+1', 'BAC+1'),
        ('BAC+2', 'BAC+2'),
        ('Licence', 'Licence'),
        ('BAC+4', 'BAC+4'),
        ('Master', 'Master'),
        ('Doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ], 'Niveau Etude', default='other', groups="hr.group_hr_user", tracking=True)
    
    qualification = fields.Char(string='Qualification')
    categorie = fields.Char(string='Categorie')
    
    rib = fields.Char(string="RIB")
    @api.depends('hiring_date')
    def _compute_seniority(self):
        today = fields.Date.today()
        today_date = fields.Date.from_string(today)
        for rec in self:
            if rec.hiring_date:
                age = today_date - fields.Date.from_string(rec.hiring_date)
                rec.seniority = int(age.days/366)
            else:
                rec.seniority = 0
                
    def _get_overtime(self, date_from, date_to):
        pass
    
    def create_employee_partner(self):
        user_group = self.env.ref("base.group_user") or False
        partner_res = self.env['res.partner']
        for record in self:
            if not record.partner_id:
                partner_id = partner_res.create({
                    'name': record.name,
                    #'partner_id': record.partner_id.id,
                    'function': record.job_id.name,
                    #'groups_id': user_group,
                    'employee': True,
                    #'customer': False,
                    'tz': self._context.get('tz'),
                })
                record.partner_id = partner_id

    
    
    