from odoo import models, fields, api, _


class ConfigReference(models.TransientModel):
    _inherit = 'res.config.settings'

    charge = fields.Integer()
   