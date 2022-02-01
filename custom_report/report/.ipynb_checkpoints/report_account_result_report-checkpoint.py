from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class ReportAccountAnalyticReportView(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.account_result_report_view'
    
    _description = 'Report Account Result'
    
    def get_code(self):
        
        res = []
        doc = []
        
        code_list = [('701400','701100%','701200%','701300%'),
                    ('701400','701100%','701200%','701300%'),
                    ('701400','701100%','701200%','701300%'),
                    ('701400','701100%','701200%','701300%'),
                    ('701400','701100%','701200%','701300%'),]
        
        for lines in code_list:
            account = self.env['account.account'].search([('code','like',lines)])
            res.append(account.code)
            

    
    def get_lines(self, analytic_id, date_start,date_end):

        query = """
                SELECT  SUM(x_aml.balance) AS x_balance_vent 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '701%') 
                AND  (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s')"""%(date_start,date_end) +"""
                UNION ALL
                SELECT  SUM(x_aml.balance) AS x_balance_achat 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '601%') 
                AND  (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s')"""%(date_start,date_end) +"""
                
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS x_balance_Variation_de_stocks_de_marchandises	
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6031%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS MARGE_COMMERCIALE		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '701%'
                        AND x_aa.code LIKE '601%'
                        AND x_aa.code LIKE '6031%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Ventes_de_produits_fabri
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE  ( x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%'
                        OR x_aa.code LIKE '702%'
                        )
                         AND (x_aml.analytic_account_id= """+ analytic_id+""") 
                         AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Travaux_services_vendus 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%') 
                         AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Produits_accessoires 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '707%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS CHIFFRE_AFFAIRES			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                         
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Production_stocke_ou_destockage 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '73%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Production_immobilisee	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '72%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Subventions_exploitation 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '71%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_produits	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE  (x_aa.code LIKE '75%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transferts_de_charges_exploitation 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '781%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Achats_de_matieres_premieres_et_fournitures_liees 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '602%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Variation_de_stocks_de_matieres_premieres_et_fournitures_liees 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6032%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_achats 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('604','605','608')) 
                        AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Variation_de_stocks_autres_approvisionnements	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6033%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transports	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '61%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Services_exterieurs 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '62%' OR x_aa.code LIKE '62%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Impots_et_taxes 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '64%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_charges 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '65%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS VALEUR_AJOUTEE			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE
                    ( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                   
                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS Charges_de_personnel 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '66%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS EXCEDENT_BRUT_EXPLOITATION			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    (( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Reprises_amortissements_de_provisions_et_depreciations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('791','798','799')) AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Dotations_aux_amortissements_aux_provisions_et_depreciations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('681','691')) AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_EXPLOITATION			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE
                    ( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%'))
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Revenus_financiers_et_assimiles 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '77%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Reprises_de_provisions_et_depreciations_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '797%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transferts_de_charges_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '787%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Frais_financiers_et_charges_assimiles 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '67%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Dotations_aux_provisions_et_aux_depreciations_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '697%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_FINANCIER		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_DES_ACTIVITES_ORDINAIRES		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    (( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        )
                    )
                    AND (( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')))
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Produits_des_cessions_immobilisations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '82%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Autres_Produits_HAO 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '84%' OR x_aa.code LIKE '86%' OR x_aa.code LIKE '88%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Valeurs_comptables_des_cessions_immobilisations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '81%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Autres_Charges_HAO 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '83%' OR x_aa.code LIKE '85%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_HORS_ACTIVITES_ORDINAIRES		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '82%'
                        OR x_aa.code LIKE '84%'
                        OR x_aa.code LIKE '86%'
                        OR x_aa.code LIKE '88%'
                        OR x_aa.code LIKE '81%'
                        OR x_aa.code LIKE '83%'
                        OR x_aa.code LIKE '85%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Participation_des_travailleurs 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '87%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Impots_sur_le_resultat 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '89%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_NET		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    ((( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        )
                    )
                    AND (( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')))
                        )
                        
                    AND ( x_aa.code LIKE '82%'
                        OR x_aa.code LIKE '84%'
                        OR x_aa.code LIKE '86%'
                        OR x_aa.code LIKE '88%'
                        OR x_aa.code LIKE '81%'
                        OR x_aa.code LIKE '83%'
                        OR x_aa.code LIKE '85%'
                        )
                    AND (x_aa.code LIKE '87%')
                    AND (x_aa.code LIKE '89%')
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)
        
        self.env.cr.execute(query)  
        
        return self.env.cr.fetchall()
      
    
    @api.model
    def _get_report_values(self, docids, data=None):
        
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        docs = []
        if data['form']['project']:
            project = data['form']['project'][0]
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            account = line.analytic_account_id.id
            id_aan = str(account)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
            
        
        return {
            'doc_model': 'account.analytic.line',
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
            'get_lines':self.get_lines,
        }

class ReportAccountAnalyticReportXlsxGenerate(models.AbstractModel):
    """
        Abstract Model specially for report template.
        _name = Use prefix `report.` along with `module_name.report_name`
    """
    _name = 'report.custom_report.account_result_report_xlsx_generate'
    _inherit = 'report.report_xlsx.abstract'
    
    _description = 'Report Account Result XLM'
    
    def get_lines(self, analytic_id, date_start,date_end):

        query = """
                SELECT  SUM(x_aml.balance) AS x_balance_vent 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '701%') 
                AND  (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s')"""%(date_start,date_end) +"""
                UNION ALL
                SELECT  SUM(x_aml.balance) AS x_balance_achat 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '601%') 
                AND  (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s')"""%(date_start,date_end) +"""
                
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS x_balance_Variation_de_stocks_de_marchandises	
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6031%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS MARGE_COMMERCIALE		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '701%'
                        AND x_aa.code LIKE '601%'
                        AND x_aa.code LIKE '6031%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Ventes_de_produits_fabri
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE  ( x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%'
                        OR x_aa.code LIKE '702%'
                        )
                         AND (x_aml.analytic_account_id= """+ analytic_id+""") 
                         AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Travaux_services_vendus 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%') 
                         AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Produits_accessoires 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '707%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS CHIFFRE_AFFAIRES			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                         
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Production_stocke_ou_destockage 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '73%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Production_immobilisee	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '72%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Subventions_exploitation 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '71%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_produits	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE  (x_aa.code LIKE '75%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transferts_de_charges_exploitation 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '781%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Achats_de_matieres_premieres_et_fournitures_liees 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '602%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Variation_de_stocks_de_matieres_premieres_et_fournitures_liees 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6032%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_achats 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('604','605','608')) 
                        AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Variation_de_stocks_autres_approvisionnements	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '6033%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transports	 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '61%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Services_exterieurs 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '62%' OR x_aa.code LIKE '62%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Impots_et_taxes 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '64%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Autres_charges 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '65%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS VALEUR_AJOUTEE			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE
                    ( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                   
                    UNION ALL
                (SELECT  SUM(x_aml.balance) AS Charges_de_personnel 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '66%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS EXCEDENT_BRUT_EXPLOITATION			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    (( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Reprises_amortissements_de_provisions_et_depreciations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('791','798','799')) AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Dotations_aux_amortissements_aux_provisions_et_depreciations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE (x_aa.code IN ('681','691')) AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_EXPLOITATION			
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE
                    ( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%'))
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Revenus_financiers_et_assimiles 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '77%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Reprises_de_provisions_et_depreciations_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '797%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Transferts_de_charges_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '787%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Frais_financiers_et_charges_assimiles 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '67%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Dotations_aux_provisions_et_aux_depreciations_financieres 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '697%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_FINANCIER		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_DES_ACTIVITES_ORDINAIRES		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    (( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        )
                    )
                    AND (( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')))
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Produits_des_cessions_immobilisations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '82%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS Autres_Produits_HAO 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '84%' OR x_aa.code LIKE '86%' OR x_aa.code LIKE '88%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                        UNION ALL
                (SELECT  SUM(x_aml.balance) AS 	Valeurs_comptables_des_cessions_immobilisations 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '81%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Autres_Charges_HAO 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '83%' OR x_aa.code LIKE '85%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_HORS_ACTIVITES_ORDINAIRES		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '82%'
                        OR x_aa.code LIKE '84%'
                        OR x_aa.code LIKE '86%'
                        OR x_aa.code LIKE '88%'
                        OR x_aa.code LIKE '81%'
                        OR x_aa.code LIKE '83%'
                        OR x_aa.code LIKE '85%'
                        ) 
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                                                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Participation_des_travailleurs 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '87%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS Impots_sur_le_resultat 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE ( x_aa.code LIKE '89%') AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)+"""
                UNION ALL
                (SELECT  SUM(x_aml.balance) AS RESULTAT_NET		
 
                FROM account_move_line AS x_aml 
                INNER JOIN account_account AS x_aa ON  x_aa.id = x_aml.account_id 
                INNER JOIN account_analytic_account AS x_aan ON x_aan.id = x_aml.analytic_account_id 
                INNER JOIN project_project AS x_pp ON x_pp.analytic_account_id = x_aml.analytic_account_id 
                WHERE 
                    ((( x_aa.code LIKE '77%'
                        OR x_aa.code LIKE '797%'
                        OR x_aa.code LIKE '787%'
                        OR x_aa.code LIKE '67%'
                        OR x_aa.code LIKE '697%'
                        )
                    )
                    AND (( x_aa.code LIKE '791%'
                        OR x_aa.code LIKE '798%'
                        OR x_aa.code LIKE '799%'
                    )
                    AND ( x_aa.code LIKE '681%'
                        OR x_aa.code LIKE '691%'
                    )
                    AND ((( (x_aa.code LIKE '701%') 
                        AND
                        (x_aa.code LIKE '702%'
                        OR x_aa.code LIKE '703%'
                        OR x_aa.code LIKE '704%')
                        
                        AND
                        
                        (x_aa.code LIKE '705%'
                        OR x_aa.code LIKE '706%')
                        AND 
                        (x_aa.code LIKE '707%')
                    ) 
                    AND (x_aa.code LIKE '601%')
                    AND (x_aa.code LIKE '6031%')

                    AND ( x_aa.code LIKE '73%'
                        OR x_aa.code LIKE '72%'
                        OR x_aa.code LIKE '71%'
                        OR x_aa.code LIKE '75%'
                        OR x_aa.code LIKE '781%'
                        OR x_aa.code LIKE '602%'
                        OR x_aa.code LIKE '6032%'
                        OR  x_aa.code LIKE '604%'
                        OR x_aa.code LIKE '605%'
                        OR  x_aa.code LIKE '608%'
                        OR x_aa.code LIKE '6033%'
                        OR  x_aa.code LIKE '61%'
                        OR x_aa.code LIKE '62%'
                        OR  x_aa.code LIKE '63%'
                        OR  x_aa.code LIKE '64%'
                        OR  x_aa.code LIKE '65%'
                        ) )
                        AND ( x_aa.code LIKE '66%')))
                        )
                        
                    AND ( x_aa.code LIKE '82%'
                        OR x_aa.code LIKE '84%'
                        OR x_aa.code LIKE '86%'
                        OR x_aa.code LIKE '88%'
                        OR x_aa.code LIKE '81%'
                        OR x_aa.code LIKE '83%'
                        OR x_aa.code LIKE '85%'
                        )
                    AND (x_aa.code LIKE '87%')
                    AND (x_aa.code LIKE '89%')
                    AND (x_aml.analytic_account_id= """+ analytic_id+""") AND (x_aml.date BETWEEN '%s' AND '%s'))

        """%(date_start,date_end)
        
        self.env.cr.execute(query)  
        
        return self.env.cr.fetchall()
    #Excel traitement
    def generate_xlsx_report(self, workbook, data, partners):
    
        sheet = workbook.add_worksheet('Account Report Result')
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})

        sheet.merge_range('A1:F1', 'Report Result', title)
        
        
        date_start = data.get('date_start')
        date_end = data.get('date_end')
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)

        docs = []
        mylist = ["Vente de Marchandise", "Achat de Marchandise", "Variation de stocks de Marchandise",
                 "MARGE  COMMERCIALE", "Ventes de produits fabriqués", "Travaux, services vendus",
                 "Produits accessoires", "CHIFFRE D'AFFAIRES", "Production stockée (ou déstockage)",
                 "Production immobilisée", "Subventions d'exploitation", "Autres produits",
                 "Transferts de charges d'exploitation", "Achats de matières premières et fournitures liées", "Variation de stocks de matières premières et fournitures liées",
                 "Autres achats", "Variation de stocks d’autres approvisionnements", "Transports",
                 "Services extérieurs", "Impôts et taxes", "Autres charges",
                 "VALEUR AJOUTEE", "Charges de personnel", "EXCEDENT BRUT D'EXPLOITATION","Reprises d’amortissements, de provisions et dépréciations",
                 "Dotations aux amortissements, aux provisions et dépréciations", "RESULTAT D'EXPLOITATION", "Revenus financiers et assimilés",
                 "Reprises de provisions et dépréciations financières", "Transferts de charges financières", "Frais financiers et charges assimilés",
                 "Dotations aux provisions et aux dépréciations financières", "RESULTAT  FINANCIER", "RESULTAT  DES ACTIVITES ORDINAIRES",
                 "Produits des cessions d'immobilisations", "Autres Produits HAO", "Valeurs comptables des cessions d'immobilisations",
                 "Autres Charges HAO", "RESULTAT HORS ACTIVITES ORDINAIRES", "Participation des travailleurs",
                 "Impôts sur le résultat", "RESULTAT NET",]
        
        if data.get('project'):
            project = data.get('project')
            lines = self.env['project.project'].search([('id','=',project)])
        else:
            lines = self.env['project.project'].search([])
        for line in lines:
            account = line.analytic_account_id.id
            id_aan = str(account)
            
            get_lines = self.get_lines(id_aan,date_start,date_end)
            name = line.name
            
            docs.append ({
                'name': name,
                'get_lines':get_lines,
            })
        
        row = 2
        col = 0
    
        # Header row
        
        sheet.write(row, col, 'Projet/Line')
        
        nombre = 0
        col +=1
        for line in docs:
            sheet.write(row, col+nombre, line['name'])
            nombre = nombre + 1
        
        row +=1
        col = 0
        i = 0
        for ligne in mylist:
            compte = 1
            for line in docs:
                sheet.write(row+i, col, ligne)
                sheet.write(row+i, col+compte, line['get_lines'][i][0])
                compte = compte + 1
            i +=1
                
        #bold = workbook.add_format({'bold': True})
        #sheet.write(0, 0, obj.name, bold)