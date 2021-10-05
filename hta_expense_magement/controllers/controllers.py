# -*- coding: utf-8 -*-
# from odoo import http


# class HtaExpenseMagement(http.Controller):
#     @http.route('/hta_expense_magement/hta_expense_magement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_expense_magement/hta_expense_magement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_expense_magement.listing', {
#             'root': '/hta_expense_magement/hta_expense_magement',
#             'objects': http.request.env['hta_expense_magement.hta_expense_magement'].search([]),
#         })

#     @http.route('/hta_expense_magement/hta_expense_magement/objects/<model("hta_expense_magement.hta_expense_magement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_expense_magement.object', {
#             'object': obj
#         })
