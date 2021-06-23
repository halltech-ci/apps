# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtaOvertimeType(models.Model):
    _name = 'hta.hr.overtime.type'
    _description = 'Overtime type'
    
    name = fields.Char()