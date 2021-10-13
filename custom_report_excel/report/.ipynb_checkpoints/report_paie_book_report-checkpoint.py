import datetime,calendar

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class ReportPaieBookExcel(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report_excel.report_paie_book_excel'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Paie Book XLM'
    
    def get_line(self, date_start, date_end, employee=None,):
        params = [date_start, date_end]
        query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                (line.date_from >= %s)
                AND (line.date_to <= %)
            """
        if employee:
            params.append([tuple(employee)])
            employee_query =  ' AND (line.employee_id = %s)'
            query = """
                SELECT * 
                FROM hr_payslip_line AS p_line
                WHERE
                (line.date_from >= %s)
                AND (line.date_to <= %) """ + employee_query + """
            """
        self.env.cr.execute(query, params)
        return self.env.cr.dictfetchall()
    
    def get_lines(self, employee, date_start,date_end):

        params = [employee,date_start,date_end]
        query = """
            SELECT hpl.name AS x_hpl_name, hpl.code AS x_hpl_code, SUM(hpl.total) AS x_hpl_total, hpl.employee_id AS x_employee
            FROM hr_payslip AS hp
            INNER JOIN hr_contract AS x_hc ON hp.contract_id = x_hc.id
            INNER JOIN hr_payslip_line AS hpl ON hpl.slip_id = hp.id
            WHERE(
                (hpl.employee_id = %s)
                AND
                (hp.date_from BETWEEN %s AND %s)
                )
            GROUP BY x_hpl_name,x_hpl_code, x_employee
            """
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
        
        
        sheet = workbook.add_worksheet('Livre de Paie')
        
        company_format = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True,})
        title = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 30,
                    'font_color': 'black', 'bold': True, 'border': 1})
        table_header = workbook.add_format(
                {'bg_color': 'white', 'align': 'center', 'font_size': 20,
                    'font_color': 'black','bold': True, 'border': 1})
        table = workbook.add_format(
                {'bg_color': 'white', 'align': 'left', 'font_size': 14,
                    'font_color': 'black','bold': True, 'border': 1})
        table_body_space = workbook.add_format(
                {'align': 'left', 'font_size': 16, 'border': 1, 'bg_color':'white', 'bold': True ,'font_color': 'black'})
        table_body_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        table_body_group_line = workbook.add_format(
                {'bg_color': 'black', 'align': 'right', 'font_size': 12,
                    'font_color': 'white', 'border': 1})
        
        sheet.set_column('A:A', 40)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:C', 30)
        sheet.set_column('D:D', 40)

        
        row = 2
        col = 0
        sheet.merge_range(row, col, row, col+3,  'Livre de Paie', title)

        date_start = data.get('date_start')
        date_end = data.get('date_end')
        
        docs = []
        
        if data.get('id_employee'):
            employee = data.get('id_employee')
            lines_contrat = self.env['hr.contract'].search([('employee_id','=',employee)])
        else:
            lines_contrat = self.env['hr.contract'].search([])
        docs = []    
        for line in lines_contrat:
            if len(line.employee_id.slip_ids)>0:
                employee = line.employee_id.id
                employee_name = line.employee_id.name
                id_he = str(employee)
                get_lines = self.get_lines(id_he,date_start,date_end)
            
                docs.append({
                    'name':employee_name,
                    'get_lines':get_lines,
                })
        
        row += 2
        col = 0
        
        # Header row
        sheet.merge_range(row, col, row, col+3, 'Rubrique', table_header)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Salaire de base', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Sursalaire', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Indemnité de congés', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Gratification/Départ', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime de responsabilité', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime de communication', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime de transport', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime de logement', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime Assurance MCI', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Autres avantages', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'SALAIRE BRUT', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prime ancienneté', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'SALAIRE BRUT IMPOSABLE', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Regime de Retraite Employe', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Regime de Retraite Patronal', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prestations Familiales', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'ASSURANCE MALADIE CMU', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Accident de Travail', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'TOTAL DES RETENUES SOCIALES', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Impots Sur Salaire (IS)', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Contribution Nationale (CN)', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Impot General Sur le Revenu (IGR)', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'TOTAL DES RETENUES FISCALES', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Formation Continue', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Taxe Apprentissage', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'TOTAL DES COTISATIONS', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'SALAIRE NET', table_body_space)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Indemnité de transport', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prelevement Assurance MCI', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Prêt', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'Avances et Acompte perçus', table)
        row += 1
        col = 0
        sheet.merge_range(row, col, row, col+3, 'NET A PAYER', table_body_space)
       

       
        
       