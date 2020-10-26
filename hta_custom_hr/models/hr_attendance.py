# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrAttendance(models.Model):
    _inherit = "hr.attendance"
    
    day_start = fields.Float(string="Day Start", default=6.5)
    project_id = fields.Many2one('project.project', string='Projet', ondelete="cascade")
    
    
    