# -*- coding: utf-8 -*-
# from odoo import http


# class WorkorderSale(http.Controller):
#     @http.route('/workorder_sale/workorder_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/workorder_sale/workorder_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('workorder_sale.listing', {
#             'root': '/workorder_sale/workorder_sale',
#             'objects': http.request.env['workorder_sale.workorder_sale'].search([]),
#         })

#     @http.route('/workorder_sale/workorder_sale/objects/<model("workorder_sale.workorder_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('workorder_sale.object', {
#             'object': obj
#         })
