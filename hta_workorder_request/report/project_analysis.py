# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class ProjectAnalysis(models.Model):
    _name = "project.analysis"
    _auto = False
    _description = "Custom project analysis"
    
    project_id = fields.Many2one('project.project', string="Projet")
    invoice_total = fields.Float(string="Total Vente")
    purchase_total = fields.Float(string="Total Achat")
    expense_total = fields.Float(string="Total Dépense")
    timesheet_total = fields.Float(string='Total Feuille de temps')
    
    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'custom_project_analysis')
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW custom_project_analysis AS (
                SELECT
        """)