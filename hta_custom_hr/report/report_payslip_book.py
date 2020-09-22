# -*- coding: utf-8 -*-

import pytz
import time
from operator import itemgetter
from itertools import groupby
from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime, date, timedelta
import re

class ReportPayslipBook(models.AbstractModel):
    _name="report.hta_custom_hr.payslip_reporting_template"#Respect naming format report.module_name.report_template_name
    _description="Payslip reporting book"
    
    
    def _get_employee_slips_lines(self, slip_id, employee_id):
        pass
    
    
    