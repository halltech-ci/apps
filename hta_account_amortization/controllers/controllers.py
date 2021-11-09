# -*- coding: utf-8 -*-
# from odoo import http


# class HtaAccountAmortization(http.Controller):
#     @http.route('/hta_account_amortization/hta_account_amortization/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_account_amortization/hta_account_amortization/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_account_amortization.listing', {
#             'root': '/hta_account_amortization/hta_account_amortization',
#             'objects': http.request.env['hta_account_amortization.hta_account_amortization'].search([]),
#         })

#     @http.route('/hta_account_amortization/hta_account_amortization/objects/<model("hta_account_amortization.hta_account_amortization"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_account_amortization.object', {
#             'object': obj
#         })
