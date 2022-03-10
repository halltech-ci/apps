# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomStock(http.Controller):
#     @http.route('/hta_custom_stock/hta_custom_stock/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_stock/hta_custom_stock/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_stock.listing', {
#             'root': '/hta_custom_stock/hta_custom_stock',
#             'objects': http.request.env['hta_custom_stock.hta_custom_stock'].search([]),
#         })

#     @http.route('/hta_custom_stock/hta_custom_stock/objects/<model("hta_custom_stock.hta_custom_stock"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_stock.object', {
#             'object': obj
#         })
