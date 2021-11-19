from odoo import models, fields, api

from odoo import models, fields, api

class WizardReportPaieBook(models.TransientModel):
    _inherit = 'paie.book.report.wizard'
    
    def get_excel(self):
        data = {
            'date_start':self.date_start,
            'date_end':self.date_end,
            'id_employee':self.id_employee.ids,
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report_excel.report_paie_book_report_xlsx').with_context(landscape=True).report_action(self, data=data)

