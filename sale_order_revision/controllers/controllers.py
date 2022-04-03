# -*- coding: utf-8 -*-
# from odoo import http


# class SaleOrderRevision(http.Controller):
#     @http.route('/sale_order_revision/sale_order_revision/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sale_order_revision/sale_order_revision/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('sale_order_revision.listing', {
#             'root': '/sale_order_revision/sale_order_revision',
#             'objects': http.request.env['sale_order_revision.sale_order_revision'].search([]),
#         })

#     @http.route('/sale_order_revision/sale_order_revision/objects/<model("sale_order_revision.sale_order_revision"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sale_order_revision.object', {
#             'object': obj
#         })
