# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.http import request


class report_module(models.Model):
    _name = 'report.hta'
    _inherit = ['mail.thread', 'mail.activity.mixin','utm.mixin','portal.mixin']
    _description = 'Report HTA'
    
    
    def action_send_mail(self):
        # self.ensure_one()
        template_id = self.env.ref('report_module.report_email_template').id
        print("Template id ", template_id)
        template =  self.env['mail.template'].browse(template_id)
        print("Template ", template)
        #template.send_mail(self.id, force_send=True)
        ctx = {
            'default_model': 'report.hta',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }



    title = fields.Char()
    reference = fields.Char(string="Reference", required=True, copy=False, readonly=True, index=True, default=lambda self:_('New'))
    objet = fields.Char()
    type = fields.Selection([
        ('internal', 'Interne'),
        ('outside', 'Externe'),
    ], string='Type de Rapport', groups="hr.group_hr_user", default='internal', tracking=True)
    client = fields.Many2one('res.partner',string='Partner',tracking=True)
    email_id = fields.Many2one('res.partner',
        string='Responsable')
    date_edit = fields.Date(string="Date", required=True, readonly=True,index=True,copy=False,
                                default=fields.Date.today())
    user_id = fields.Many2one(comodel_name='res.users', string="Utilisateur", readonly=True,
                              default=lambda self: self.env.uid)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    sale_id = fields.Many2one('sale.order', string='Devis')
    project_id = fields.Many2one('project.project', string='Projet')
    note = fields.Html()
    reste = fields.Html()
    bloquant = fields.Html()

    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('reference.code') or _('New')

        result = super(report_module, self).create(vals)
        return result





