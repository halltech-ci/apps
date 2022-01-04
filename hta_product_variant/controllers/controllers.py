# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProductVariant(http.Controller):
#     @http.route('/hta_product_variant/hta_product_variant/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_product_variant/hta_product_variant/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_product_variant.listing', {
#             'root': '/hta_product_variant/hta_product_variant',
#             'objects': http.request.env['hta_product_variant.hta_product_variant'].search([]),
#         })

#     @http.route('/hta_product_variant/hta_product_variant/objects/<model("hta_product_variant.hta_product_variant"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_product_variant.object', {
#             'object': obj
#         })
