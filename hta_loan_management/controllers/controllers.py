# -*- coding: utf-8 -*-
# from odoo import http


# class HtaLoanManagement(http.Controller):
#     @http.route('/hta_loan_management/hta_loan_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_loan_management/hta_loan_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_loan_management.listing', {
#             'root': '/hta_loan_management/hta_loan_management',
#             'objects': http.request.env['hta_loan_management.hta_loan_management'].search([]),
#         })

#     @http.route('/hta_loan_management/hta_loan_management/objects/<model("hta_loan_management.hta_loan_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_loan_management.object', {
#             'object': obj
#         })
