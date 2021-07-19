# -*- coding: utf-8 -*-
# Part of Aktiv Software
# See LICENSE file for full copyright & licensing details.

from odoo import models

class PartnerXlsx(models.AbstractModel):
    _name = 'report.hta_sale_excel_report.sale_xlsx'
    _description = 'Sale Oder Excle Report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        for obj in partners:
            customer_data = ''
            company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 25,
                    'font_color': 'black'})
            order_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black', 'bold': True, 'border': 1})
            description_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black', 'border': 1})
            destination_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black',})
            table_header_left = workbook.add_format(
                {'bg_color': 'black', 'align': 'left', 'font_size': 12,
                    'font_color': 'white'})
            table_row_left = workbook.add_format(
                {'align': 'left', 'font_size': 12, 'border': 1})
            table_header_right = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
            table_row_right = workbook.add_format(
                {'align': 'right', 'font_size': 12, 'border': 1})
            customer_header_format = workbook.add_format({
                'align': 'center', 'font_size': 13, 'bold': True, 'border': 1})
            customer_format = workbook.add_format({
                'align': 'center', 'font_size': 13, 'border': 1})
            reference_format = workbook.add_format({
                'align': 'left', 'font_size': 12,})
            table_left = workbook.add_format(
                {'align': 'left', 'bold': True, 'border': 1})
            table_right = workbook.add_format(
                {'align': 'right', 'bold': True, 'border': 1})
            
            
            if obj.partner_id.name:
                customer_data += obj.partner_id.name + '\n'
            if obj.partner_id.street:
                customer_data += obj.partner_id.street + '\n'
            if obj.partner_id.street2:
                customer_data += obj.partner_id.street2 + '\n'
            if obj.partner_id.city:
                customer_data += obj.partner_id.city + ' '
            if obj.partner_id.state_id:
                customer_data += str(obj.partner_id.state_id.name + ' ')
            if obj.partner_id.zip:
                customer_data += obj.partner_id.zip + ' '
            if obj.partner_id.country_id:
                customer_data += '\n' + str(obj.partner_id.country_id.name)
            worksheet = workbook.add_worksheet(obj.name)
            worksheet.set_column('A:A', 40)
            worksheet.merge_range('A1:I3', obj.company_id.name, company_format)
            worksheet.merge_range('E4:I5', customer_data, customer_header_format)
            worksheet.merge_range('A6:I6', '')
            worksheet.merge_range('A7:I8', 'DEVIS/QUOTATION : ' + obj.name, order_format)
            worksheet.merge_range('A9:I9', '')
            worksheet.merge_range('A10:B10', 'Date : ' + str(obj.date_order.date()), destination_format)
            if obj.sale_order_recipient:
                worksheet.merge_range('E10:I10', 'Destinataire : ' + obj.sale_order_recipient, destination_format)
            if obj.project_code:
                worksheet.merge_range('C10:D10', 'Projet : ' + str(obj.project_code), destination_format)
            worksheet.merge_range('A11:I11', '')
            if obj.client_order_ref:
                worksheet.merge_range(
                    'A12:D12', 'Référence Client : ' +obj.client_order_ref, reference_format)
                if obj.payment_term_id:
                    worksheet.merge_range(
                        'E12:I12', 'Payment Terms: ' +obj.payment_term_id.name, reference_format)
            elif obj.payment_term_id:
                worksheet.merge_range(
                    'E12:I12', 'Payment Terms: ' +obj.payment_term_id.name, reference_format)
            worksheet.merge_range('A13:I13', '')
            worksheet.merge_range('A14:I14', 'Objet : ' + str(obj.description), description_format)
            worksheet.set_column('B:B', 15)
            worksheet.set_column('C:C', 15)
            worksheet.set_column('D:D', 15)
            worksheet.set_column('E:E', 15)
            worksheet.set_column('F:F', 15)
            worksheet.set_column('G:G', 15)
            worksheet.set_column('H:H', 15)
            worksheet.set_column('I:I', 15)
            row = 14
            group = self.env.user.has_group(
                'product.group_discount_per_so_line')
            display_discount = any([l.discount for l in obj.order_line])
            display_tax = any([l.tax_id for l in obj.order_line])
            worksheet.write(row, 0, 'Article', table_header_left)
            worksheet.write(row, 1, 'Quantité', table_header_right)
            worksheet.write(row, 2, 'Unité', table_header_right)
            worksheet.write(row, 3, 'Coût', table_header_right)
            worksheet.write(row, 4, 'Marge(%)', table_header_right)
            worksheet.write(row, 5, 'Prix Unitaire', table_header_right)
            worksheet.write(row, 6, 'Prix Total', table_header_right)
            if display_discount and group:
                worksheet.write(row, 7, 'Remise(%)', table_header_right)
                worksheet.write(row, 8, 'Sous Total', table_header_right)
            row += 1

            for line in obj.order_line:
                if not line.display_type:
                    worksheet.write(row, 0, line.name, table_row_left)
                    worksheet.write(row, 1, line.product_uom_qty, table_row_right)
                    worksheet.write(row, 2, line.product_uom.name, table_row_right)
                    worksheet.write(row, 3, line.product_cost, table_row_right)
                    worksheet.write(row, 4, line.line_margin, table_row_right)
                    worksheet.write(row, 5, line.line_subtotal, table_row_right)
                    worksheet.write(row, 6, line.price_unit, table_row_right)
                    if display_discount and group:
                        worksheet.write(row, 7, line.discount, table_row_right)
                        worksheet.write(row, 8, line.price_subtotal, table_row_right)
                    row += 1
                if line.display_type == 'line_section':
                    worksheet.merge_range(row, 0, row, 6, line.name, table_row_left)
                    row += 1
                if line.display_type == 'line_note':
                    worksheet.merge_range(row, 0, row, 6, line.name, table_row_left)
                    row += 1
            if display_discount and group and display_tax:
                worksheet.merge_range(row, 0, row, 8, '')
                worksheet.write(row + 1, 7, 'Montant HT', table_left)
                worksheet.write(row + 1, 8, obj.amount_total_no_tax, table_right)
                worksheet.write(row + 2, 7, 'Remise', table_left)
                worksheet.write(row + 2, 8, obj.remise_total, table_right)
                worksheet.write(row + 3, 7, 'Total HT', table_left)
                worksheet.write(row + 3, 8, obj.amount_untaxed, table_right)
                worksheet.write(row + 4, 7, 'Taxes', table_left)
                worksheet.write(row + 4, 8, obj.amount_tax, table_right)
                worksheet.write(row + 5, 7, 'Total TTC', table_left)
                worksheet.write(row + 5, 8, obj.amount_total, table_right)
            elif not group and not display_tax and not display_discount:
                worksheet.merge_range(row, 0, row, 6, '')
                worksheet.write(row + 1, 5, 'Total HT', table_left)
                worksheet.write(row + 1, 6, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 5, 'Total', table_left)
                worksheet.write(row + 2, 6, obj.amount_total, table_right)
            elif not group and not display_tax:
                worksheet.merge_range(row, 0, row, 3, '')
                worksheet.write(row + 1, 2, 'Subtotal', table_left)
                worksheet.write(row + 1, 3, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 2, 'Total', table_left)
                worksheet.write(row + 2, 3, obj.amount_total, table_right)
            elif not display_tax and not display_discount:
                worksheet.merge_range(row, 0, row, 6, '')
                worksheet.write(row + 1, 5, 'Total HT', table_left)
                worksheet.write(row + 1, 6, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 5, 'Total', table_left)
                worksheet.write(row + 2, 6, obj.amount_total, table_right)
            elif group and display_discount:
                worksheet.merge_range(row, 0, row, 8, '')
                worksheet.write(row + 1, 7, 'Montant HT', table_left)
                worksheet.write(row + 1, 8, obj.amount_total_no_tax, table_right)
                worksheet.write(row + 2, 7, 'Remise', table_left)
                worksheet.write(row + 2, 8, obj.remise_total, table_right)
                worksheet.write(row + 3, 7, 'Total HT', table_left)
                worksheet.write(row + 3, 8, obj.amount_untaxed, table_right)
                worksheet.write(row + 4, 7, 'Total TTC', table_left)
                worksheet.write(row + 4, 8, obj.amount_total, table_right)
            elif display_tax:
                worksheet.merge_range(row, 0, row, 6, '')
                worksheet.write(row + 1, 5, 'Subtotal', table_left)
                worksheet.write(row + 1, 6, obj.amount_untaxed, table_right)
                worksheet.write(row + 2, 5, 'Taxes', table_left)
                worksheet.write(row + 2, 6, obj.amount_tax, table_right)
                worksheet.write(row + 3, 5, 'Total', table_left)
                worksheet.write(row + 3, 6, obj.amount_total, table_right)
            worksheet.merge_range(row + 4, 0, row + 4, 5, '')
            worksheet.merge_range(row + 5, 0, row + 5, 5, obj.amount_to_word, destination_format)
            worksheet.write(row + 7, 5, str(obj.signed_user.name), destination_format)