# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    hta_doc_signature = fields.Binary(string="Signature Document")
    hta_doc_initials = fields.Binary(string="Signature Initials")