# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    approve_limit_1 = fields.Monetary(related="company_id.approve_limit_1")
    approve_limit_2 = fields.Monetary(related="company_id.approve_limit_2")
