# -*- coding: utf-8 -*-
# from odoo import http


# class HtaPurchaseType(http.Controller):
#     @http.route('/hta_purchase_type/hta_purchase_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_purchase_type/hta_purchase_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_purchase_type.listing', {
#             'root': '/hta_purchase_type/hta_purchase_type',
#             'objects': http.request.env['hta_purchase_type.hta_purchase_type'].search([]),
#         })

#     @http.route('/hta_purchase_type/hta_purchase_type/objects/<model("hta_purchase_type.hta_purchase_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_purchase_type.object', {
#             'object': obj
#         })
