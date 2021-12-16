# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PartnerXlsx(models.AbstractModel):
    _name = 'report.custom_invoice.report_invoice_xlsx'
    _description = 'Facture Report Excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        sheet = workbook.add_worksheet('Patner ID')
        bold = workbook.add_format({'bold': True})
        header1_fotmat = workbook.add_format({'align': 'center', 'font_size': 40, 'border': 2})
        header2_fotmat = workbook.add_format({'align': 'center', 'font_size': 14, 'border': 1})
        date_fotmat = workbook.add_format({'align': 'center', 'font_size': 14,})
        position_fotmat = workbook.add_format({'align': 'center', 'font_size': 12})
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'font_size': 14})
        client_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 15})
        line_formart = workbook.add_format({'align': 'center', 'font_size': 12})
    
        row = 0
        row1 = 0
        col = 0
        i = 2
        sheet.set_column('A:A',60)
        sheet.set_column('B:B',20)
        sheet.set_column('C:C',25)
        sheet.set_column('D:D',25)
        for obj in partners:
            row1 +=6
            sheet.merge_range(row1, col+2,row1, col+3, 'Abibjan le : ' + str(obj.invoice_date), date_fotmat)
            sheet.merge_range(row1+1, col+2,row1+7, col+3, 'hgdhgdsfgdsfhgdsfhgdsfhg', header2_fotmat)
            sheet.write(row1+4, col+1, 'Client',  client_format)
            
            row1 += 10
            sheet.write(row1, col, 'Description', header_format)
            sheet.write(row1, col+1, 'Quantité', header_format)
            sheet.write(row1, col+2, 'Prix Unitaire', header_format)
            sheet.write(row1, col+3, 'Montant', header_format)
            
            for line in obj.invoice_line_ids:
                sheet.write(row1+i, col, line.name, line_formart)
                sheet.write(row1+i, col+1, line.quantity, line_formart)
                sheet.write(row1+i, col+2, line.price_unit, line_formart)
                sheet.write(row1+i, col+3, line.price_total, line_formart)
                
                i +=1
                
              