# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import tools

class ProjectAnalysis(models.Model):
    _name = "project.analysis"
    _auto = False
    _description = "Custom project analysis"
    
    project_id = fields.Many2one('project.project', string="Projet")
    sale_total = fields.Float(string="Total Vente")#sale.order (project_id)
    #stock_move = fields.Many2one('stock.move')#Total matière
    stock_move_total = fields.Float(string="Total coüt matière")#stock.move
    expense_total = fields.Float(string="Total Dépense")#expense.request
    sub_contract = fields.Float(string='Sous Traitance')#purchase.order
    timesheet_total = fields.Float(string='Total Feuille de temps')#
    exclude_from_invoice_tab = fields.Boolean('Exclude from invoice')
    
    """
    table (project.project): project_id, 
    table (sale.order) : project_id ==> total_sale (total vente)
    table (stock.move) : project_id ==> stock_move total matière
    table (expense.request) : project_id ==> expense_total 
    """
    
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
                    exclude_from_invoice_tab FROM (
                        SELECT
                            p.id as project_id,
                            am.amount_untaxed as invoice_total,
                            
                    )
        """)