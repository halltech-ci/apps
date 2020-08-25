# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class hta_custom_hr(models.Model):
#     _name = 'hta_custom_hr.hta_custom_hr'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100

class HrContract(models.Model):
    _inherit = "hr.contract"
    
    hourly_rate = fields.Monetary(string="Taux Horaire", compute="_compute_employee_hourly_rate")
    prime_transport = fields.Monetary(string="Prime de Transport")
    prime_communication = fields.Monetary(string="Prime de Communication")
    sursalaire = fields.Monetary(string="Sursalaire")
    prime_logement = fields.Monetary(string="Prime de logement")
    prime_responsabilite = fields.Monetary(string="Prime de responsabilité")
    gratification = fields.Monetary(string="Gratification")
    autres_avantages = fields.Monetary(string="Autres Avantages")
    conges_payes = fields.Monetary(string="Congés Payés")
    
    
    @api.depends("wage")
    def _compute_employee_hourly_rate(self):
        for rec in self:
            rec.hourly_rate = rec.wage/173.33
    
    
    