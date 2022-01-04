# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductDefaultCode(http.Controller):
#     @http.route('/hta_product_default_code/hta_product_default_code/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_default_code/hta_product_default_code/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_default_code.listing', {
#             'root': '/hta_product_default_code/hta_product_default_code',
#             'objects': http.request.env['hta_product_default_code.hta_product_default_code'].search([]),
#         })

#     @http.route('/hta_product_default_code/hta_product_default_code/objects/<model("hta_product_default_code.hta_product_default_code"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_default_code.object', {
#             'object': obj
#         })
