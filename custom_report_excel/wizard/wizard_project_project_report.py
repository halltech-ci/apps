from odoo import models, fields, api

from odoo import models, fields, api

class WizardReportProject(models.TransientModel):
    _inherit = 'project.project.report.wizard'
    
    def get_excel(self):
        data = {
            'date_start':self.date_start,
            'date_end':self.date_end,
            'project':self.project.id,
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report_excel.report_project_report_xlsx').with_context(landscape=True).report_action(self, data=data)

