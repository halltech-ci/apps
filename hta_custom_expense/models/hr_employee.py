# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    @api.multi
    def name_get(self):
        result = []
        matricule = ''
        for rec in self:
            name = rec.name
            name_matricule = name
            if rec.matricule:
                matricule = rec.matricule
                name_matricule = '{0} - {1}'.format(name, matricule)
            result.append((rec.id, name_matricule))
        return result
            