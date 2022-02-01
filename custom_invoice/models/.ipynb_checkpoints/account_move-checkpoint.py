# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError

class AccountMove(models.Model):
    _inherit = "account.move"
    
    #num2words convert number to word
    def _num_to_words(self, num):
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()
        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""
        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].with_context(active_test=False).search([('code', '=', lang_code)])
        num_to_word = _num2words(num, lang=lang.iso_code)
        return num_to_word
    
    delivery_slip=fields.Char(string='N° Bordereau de Livraison')
    customer_reference=fields.Char(string='Ref. Commande Client')
    signataire_facture=fields.Many2one('res.users', string='Signataire')
    invoice_object=fields.Char(string='Objet :')
    source_document=fields.Char(string='N° Bon de commande :')
    amount_to_word = fields.Char(string="Amount In Words:", compute='_compute_amount_to_word')
    
    def _compute_amount_to_word(self):
        for rec in self:
            rec.amount_to_word = str(self._num_to_words(rec.amount_total)).upper()
            
            
            
class PartnerXlsx(models.AbstractModel):
    _name = 'report.custom_invoice.report_invoice_xlsx'
    _description = 'Facture Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Patner ID')
        bold = workbook.add_format({'bold': True})
        row = 10
        col = 0
        sheet.set_column('A:A',12)
        sheet.set_column('B:B',12)
        sheet.set_column('C:C',15)
        sheet.set_column('D:D',20)
        sheet.set_column('E:E',15)
        sheet.set_column('F:F',12)
        sheet.set_column('G:G',12)
        sheet.set_column('H:H',15)
        sheet.set_column('I:I',12)
        sheet.set_column('J:J',15)
        sheet.set_column('K:K',12)
        for obj in partners:
            row += 1
            sheet.write(10,0, 'Numero',bold)
            sheet.write(row, col, obj.name)
            sheet.write(10,1, 'Customer',bold)
            sheet.write(row, col +1, obj.invoice_partner_display_name)           
            sheet.write(10,2, 'Invoice Date',bold)
            sheet.write(row, col +2, obj.invoice_date)           
            sheet.write(10,3, 'Source Document',bold)
            sheet.write(row, col +3, obj.invoice_origin)    
            #sheet.write(10,4, 'Sales Persons',bold)
            #sheet.write(row, col +1, obj.invoice_user_id)            
            #sheet.write(10,5, 'Company',bold)
            #sheet.write(row, col +1, obj.company_id)           
            #sheet.write(10,6, 'Due Date',bold)
            #sheet.write(row, col +1, obj.invoice_date_due)            
            #sheet.write(10,7, 'Tax Excluded',bold)
            #sheet.write(row, col +1, obj.amount_untaxed_signed)            
            #sheet.write(10,8, 'Total',bold)
            #sheet.write(row, col +1, obj.amount_total_signed)           
            #sheet.write(10,9, 'Amount Due',bold)
            #sheet.write(row, col +1, obj.amount_residual_signed)          
            #sheet.write(10,10, 'Status',bold)
            #sheet.write(row, col +1, obj.state)
            
           
            
            
            
   