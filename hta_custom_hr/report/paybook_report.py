# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class PaybookReport(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.hta_custom_hr.paybook_template'
    _description = 'Report Paie Book'