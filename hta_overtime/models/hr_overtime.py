# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HtaOvertime(models.Model):
    _name = 'hta.hr.overtime'
    _description = 'Custom overtime management'

    name = fields.Char()
    