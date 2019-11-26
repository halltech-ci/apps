# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models


class Project(models.Model):
    _inherit = 'project.project'

    purchase_request_ids = fields.One2many(string='Purchase', comodel_name='purchase.request',
        inverse_name='project_id'
    )
    

    