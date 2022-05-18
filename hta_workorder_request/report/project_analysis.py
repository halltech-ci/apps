# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class ProjectAnalysis(models.Model):
    _name = "project.analysis"
    _auto = False
    _description = "Custom project analysis"
    
    project_id = fields.Many2one('project.project', string="Projet")
    invoice_total = fields.Float(string="Total Vente")#Bon de commande
    purchase_total = fields.Float(string="Total coüt matière")#consommation de matière imputée au projet stock.move ou stock.move.line
    expense_total = fields.Float(string="Total Dépense")#expense_line
    sub_contract = fields.Float(string='Sous Traitance')#
    timesheet_total = fields.Float(string='Total Feuille de temps')
    exclude_from_invoice_tab = fields.Boolean('Exclude from invoice')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'custom_project_analysis')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW custom_project_analysis AS (
                SELECT 
                    row_number() OVER () AS id,
                    project_id,
                    invoice_toal,
                    purchase_total,
                    expense_total,
                    sub_contract,
                    timesheet_total,
                    
        """)