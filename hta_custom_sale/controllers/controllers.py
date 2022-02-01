# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomSale(http.Controller):
#     @http.route('/hta_custom_sale/hta_custom_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_sale/hta_custom_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_sale.listing', {
#             'root': '/hta_custom_sale/hta_custom_sale',
#             'objects': http.request.env['hta_custom_sale.hta_custom_sale'].search([]),
#         })

#     @http.route('/hta_custom_sale/hta_custom_sale/objects/<model("hta_custom_sale.hta_custom_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_sale.object', {
#             'object': obj
#         })
