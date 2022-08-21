# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseWorkAcceptance(http.Controller):
#     @http.route('/purchase_work_acceptance/purchase_work_acceptance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_work_acceptance/purchase_work_acceptance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_work_acceptance.listing', {
#             'root': '/purchase_work_acceptance/purchase_work_acceptance',
#             'objects': http.request.env['purchase_work_acceptance.purchase_work_acceptance'].search([]),
#         })

#     @http.route('/purchase_work_acceptance/purchase_work_acceptance/objects/<model("purchase_work_acceptance.purchase_work_acceptance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_work_acceptance.object', {
#             'object': obj
#         })
