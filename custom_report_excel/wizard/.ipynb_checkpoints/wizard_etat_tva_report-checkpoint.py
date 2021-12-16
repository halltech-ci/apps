from odoo import models, fields, api

from odoo import models, fields, api

class EtatTvaReportWizard(models.TransientModel):
    _inherit = 'etat.tva.report.wizard'
    
    def get_excel(self):
        data = {
            'date_start':self.date_start,
            'date_end':self.date_end,
            'partner':self.partner.ids,
        }
        # ref `module_name.report_id` as reference.
        return self.env.ref('custom_report_excel.etat_tva_analytic_report_xlsx').with_context(landscape=True).report_action(self, data=data)
