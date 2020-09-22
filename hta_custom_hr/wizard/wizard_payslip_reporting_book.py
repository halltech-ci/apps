# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from io import BytesIO
import xlwt
import base64
from datetime import datetime, date


class PayslipReportingBook(models.TransientModel):
    _name="payslip.reporting.book"
    _description="Wizard payslip reporting book"
    
    start_date = fields.Date(string="From Date", default=fields.Date.today())
    end_date = fields.Date(string="Today", required=True, default=fields.Date.today())
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id, required=True)
    
    def check_date_range(self):
        if self.end_date <= self.start_date:
            raise ValidationError(_('Enter proper date range'))
    
    @api.multi
    def generate_pdf_report(self):
        self.check_date_range()
        #self.check_period_range()
        datas = {'form':
            {
                'company_id': self.company_id.id,
                #'warehouse_ids': [y.id for y in self.warehouse_ids],
                #'location_id': self.location_id and self.location_id.id or False,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'id': self.id,
                #'product_ids': self.product_ids.ids,
                #'product_categ_ids': self.category_ids.ids
            },
        }
        return self.env.ref('hta_custom_hr.action_payslip_reporting_book').report_action(self, data=datas)
    
    @api.multi
    def generate_xls_report(self):
        self.check_date_range()
        pass
