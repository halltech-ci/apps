# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"
    
    request_order = fields.Many2one('stock.request.order')
    use_cost = fields.Float('Use Cost')
    use_time = fields.Float('Use Time')