# -*- coding: utf-8 -*-

from odoo import models, fields, api,_

class hta_report(models.Model):
    _name = 'hta_custom_report'
    _description = 'hta_report.hta_report'
    _inherit = ['mail.thread','mail.activity.mixin']
    
    title = fields.Char()
    utilisateur = fields.Many2one(comodel_name='res.users', default=lambda self: self.env.uid)
    societe = fields.Many2one(comodel_name='res.company', default=lambda self: self.env.company)
    responsable = fields.Many2one(comodel_name='res.partner')
    date_saisir = fields.Date(default=fields.Date.today())
    note = fields.Html("Note", required=True)
    reste_gerer = fields.Html("Reste à Gérer", required=True)
    bloquante = fields.Html("Les elements Bloquants", required=True)
    report_reference = fields.Char(string='Rapport Reference', required=True, copy=False, readonly=True, index=True,default=lambda self: _('New'))
    date_now = fields.Datetime(default=fields.Datetime.now())
    objet = fields.Text()
    commande = fields.Binary()


    
    @api.model
    def create(self, vals):
        if vals.get('report_reference', _('New')) == _('New'):
            vals['report_reference'] = self.env['ir.sequence'].next_by_code('rapport_reference.code') or _('New')
        result = super(hta_report, self).create(vals)
        return result
    
    
    def action_send_mail(self):
        self.ensure_one()
        template_id = self.env.ref('hta_report.email_template_report_view').id
        ctx = {
            'default_model':'hta_custom_report',
            'default_res_id':self.id,
            'default_use_template': bool(template_id),
            'default_template_id':template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent':True,
            'force_email':True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode':'form',
            'res_model':'mail.compose.message',
            'views':[(False,'form')],
            'view_id':False,
            'target':'new',
            'context':ctx,
        }