# -*- coding: utf-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

from odoo.addons import decimal_precision as dp



class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    asset_starting_date = fields.Date('Asset Starting date', default=fields.Date.context_today)
    
    @api.one
    @api.depends('asset_category_id', 'asset_starting_date')
    def _get_asset_date(self):
        self.asset_mrr = 0
        #self.asset_start_date = False
        start_date = datetime.strptime(self.asset_starting_date, DF).replace(day=1)
        self.asset_start_date = start_date.strftime(DF)
        self.asset_end_date = False
        cat = self.asset_category_id
        if cat:
            if cat.method_number == 0 or cat.method_period == 0:
                raise UserError(_('The number of depreciations or the period length of your asset category cannot be null.'))
            months = cat.method_number * cat.method_period
            if self.invoice_id.type in ['out_invoice', 'out_refund']:
                self.asset_mrr = self.price_subtotal_signed / months
            if self.invoice_id.date_invoice:
                end_date = (start_date + relativedelta(months=months, days=-1))
                self.asset_end_date = end_date.strftime(DF)
