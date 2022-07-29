# -*- coding: utf-8 -*-
# from odoo import http


# class PurchaseRequestStatus(http.Controller):
#     @http.route('/purchase_request_status/purchase_request_status/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_request_status/purchase_request_status/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_request_status.listing', {
#             'root': '/purchase_request_status/purchase_request_status',
#             'objects': http.request.env['purchase_request_status.purchase_request_status'].search([]),
#         })

#     @http.route('/purchase_request_status/purchase_request_status/objects/<model("purchase_request_status.purchase_request_status"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_request_status.object', {
#             'object': obj
#         })
