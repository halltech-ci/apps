# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrWorkEntryType(models.Model):
    _inherit = "hr.work.entry.type"
    
    to_be_paid = fields.Boolean(string = 'To be Paid', default=False)