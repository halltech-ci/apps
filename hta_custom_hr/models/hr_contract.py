# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HrContract(models.Model):
    _inherit = "hr.contract"
    
    #hourly_rate = fields.Monetary(string="Taux Horaire", compute="_compute_employee_hourly_rate")
    prime_transport = fields.Monetary(string="Prime de Transport")
    indemnite_transport = fields.Monetary(string="Indemnité de Transport")
    indemnite_licencement = fields.Monetary(string="Indemnité de Licencement")
    indemnite_compensatrice = fields.Monetary(string="Indemnité de compensatrice préavis ")
    indemnite_conge = fields.Monetary(string="Indemnité de conge")
    prelevement_assurance_mci = fields.Monetary(string="Prélèvement Assurance Employé")
    pret = fields.Monetary(string="Prêt")
    prime_assurance_mci = fields.Monetary(string="Part Assurance Employeur")
    prime_communication = fields.Monetary(string="Communication")
    sursalaire = fields.Monetary(string="Sursalaire")
    prime_logement = fields.Monetary(string="Logement")
    prime_responsabilite = fields.Monetary(string="Responsabilité")
    prime_rendement = fields.Monetary(string="Prime de rendement")
    prime_salissure = fields.Monetary(string="Salissure")
    gratification = fields.Monetary(string="Gratification")
    autres_avantages = fields.Monetary(string="Autres Avantages")
    conges_payes = fields.Monetary(string="Congés Payés")
    salaire_brut = fields.Monetary(string="Salary Cost")
    salaire_base = fields.Monetary(string="Salary Base")
    avs = fields.Monetary(string="Avances et  Acomptes perçus")
    partner_id = fields.Many2one('res.partner', string="Partner")
    holidays = fields.Float(string='Paid Time Off',
        help="Number of days of paid leaves the employee gets per year."
    )
    communication_flotte = fields.Monetary(string="Coût Communication Flotte")
    #Traitement special AVS, pret
    
    loan_account = fields.Many2one('account.account', 'Loan Account', company_dependent=True, domain=[('deprecated', '=', False)])
    advance_account = fields.Many2one('account.account', 'Advance Account', company_dependent=True, domain=[('deprecated', '=', False)])

    #line amount loan
    hr_loan_employee_ids = fields.One2many("hr.loan.employee", "hr_contract_id", string="Loan of employee")
    
    # Account 
    account_debit = fields.Many2one('account.account', 'Debit Account', company_dependent=True, domain=[('deprecated', '=', False)])
    account_credit = fields.Many2one('account.account', 'Credit Account', company_dependent=True, domain=[('deprecated', '=', False)])
