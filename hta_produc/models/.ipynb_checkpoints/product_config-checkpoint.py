from odoo import _, api, fields, models 


class ConfigReference(models.TransientModel):
    _inherit = 'res.config.settings'

    charge = fields.Integer()