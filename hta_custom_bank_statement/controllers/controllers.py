# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomBankStatement(http.Controller):
#     @http.route('/hta_custom_bank_statement/hta_custom_bank_statement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_bank_statement/hta_custom_bank_statement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_bank_statement.listing', {
#             'root': '/hta_custom_bank_statement/hta_custom_bank_statement',
#             'objects': http.request.env['hta_custom_bank_statement.hta_custom_bank_statement'].search([]),
#         })

#     @http.route('/hta_custom_bank_statement/hta_custom_bank_statement/objects/<model("hta_custom_bank_statement.hta_custom_bank_statement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_bank_statement.object', {
#             'object': obj
#         })
