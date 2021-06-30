# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtaOvertimeType(models.Model):
    _name = 'hta.hr.overtime.type'
    _description = 'Overtime type'
    
    name = fields.Char()
    validation_type = fields.Selection([
        ('no_validation', 'No Validation'),
        ('hr', 'Overtime Officer'),
        ('manager', 'Team Leader'),
        ('both', 'Team Leader and Overtime Officer')], default='hr', string='Validation')