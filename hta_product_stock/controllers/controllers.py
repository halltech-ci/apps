# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductStock(http.Controller):
#     @http.route('/hta_product_stock/hta_product_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_stock/hta_product_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_stock.listing', {
#             'root': '/hta_product_stock/hta_product_stock',
#             'objects': http.request.env['hta_product_stock.hta_product_stock'].search([]),
#         })

#     @http.route('/hta_product_stock/hta_product_stock/objects/<model("hta_product_stock.hta_product_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_stock.object', {
#             'object': obj
#         })
