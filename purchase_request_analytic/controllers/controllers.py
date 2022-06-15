# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRequestAnalytic(http.Controller):
#     @http.route('/purchase_request_analytic/purchase_request_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_request_analytic/purchase_request_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_request_analytic.listing', {
#             'root': '/purchase_request_analytic/purchase_request_analytic',
#             'objects': http.request.env['purchase_request_analytic.purchase_request_analytic'].search([]),
#         })

#     @http.route('/purchase_request_analytic/purchase_request_analytic/objects/<model("purchase_request_analytic.purchase_request_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_request_analytic.object', {
#             'object': obj
#         })
