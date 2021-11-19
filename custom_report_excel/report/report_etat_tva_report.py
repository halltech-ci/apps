import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReporEtatTvaReportExcel(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.report_etat_tva_report_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Etat Tva Report XLM'


    def get_lines(self, partner_id, date_start,date_end):
        
        params = [tuple(partner_id),date_start,date_end]
        query = """
                SELECT rp.name AS partner, am.ref AS refence, am.date AS x_date, SUM(am.amount_total) AS total, SUM(am.amount_tax) AS tax
                FROM account_move AS am
                INNER JOIN res_partner AS rp ON rp.id = am.partner_id
                WHERE
                    (am.type LIKE '%invoice%')
                    AND
                    (am.partner_id = """+partner_id+""")
                    AND
                    (am.date BETWEEN '%s' AND '%s')

                GROUP BY partner,refence,x_date
        """%(date_start,date_end)

        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Etat Tva Report ')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 21,
                    'font_color': 'black', 'bold': True, 'border': 1})
        table_header = workbook.add_format(
                {'bg_color': '#8f8e8d', 'align': 'center', 'font_size': 11,
                    'font_color': 'black','bold': True,})
        table_body_space = workbook.add_format(
                {'align': 'center', 'font_size': 12})
        table_body_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        sheet.set_column('A:A', 40)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 25)
        sheet.set_column('D:D', 25)
        sheet.set_column('E:E', 25)
        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+4,  'TVA Rapport', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        if data.get('partner'):
            partner = data.get('partner')
            lines = self.env['res.partner'].search([('id','=',partner)])
        else:
            lines = self.env['res.partner'].search([])
        for line in lines:
            partner_id = line.id
            id_rp = str(partner_id)
            
            get_lines = self.get_lines(id_rp,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
           
        row += 2
        col = 0
        
        # Header row
        sheet.merge_range(row, col, row+1, col, 'Partner', table_header)
        sheet.merge_range(row, col+1, row+1, col+1, 'Reference', table_header)
        sheet.merge_range(row, col+2, row+1, col+2, 'date', table_header)
        sheet.merge_range(row, col+3, row+1, col+3, 'date', table_header)
        sheet.merge_range(row, col+4, row+1, col+4, 'Tax', table_header)
        
        ligne = 5
        j = 0
        i = 1
        for line in docs:
            for partner in line['get_lines']:
                sheet.write(ligne+i, col, analytic.get('partner'),table_body_space)
                sheet.write(ligne+i, col+1, analytic.get('refence'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('x_date'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('total'),table_body_space)
                sheet.write(ligne+i, col+2, analytic.get('tax'),table_body_space)