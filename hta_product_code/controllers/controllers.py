# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductCode(http.Controller):
#     @http.route('/hta_product_code/hta_product_code/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_code/hta_product_code/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_code.listing', {
#             'root': '/hta_product_code/hta_product_code',
#             'objects': http.request.env['hta_product_code.hta_product_code'].search([]),
#         })

#     @http.route('/hta_product_code/hta_product_code/objects/<model("hta_product_code.hta_product_code"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_code.object', {
#             'object': obj
#         })
