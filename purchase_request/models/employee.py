from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError

class HrEmployee(models.Model):
    _inherit = "hr.employee"
    
    
    project_approver = fields.Boolean(string="Is Project Approver", default=False)