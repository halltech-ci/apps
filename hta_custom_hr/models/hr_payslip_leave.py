# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import datetime

class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    
    def _get_contract_wage(self):
        self.ensure_one()
        return self.contract_id.salaire_base
    
    