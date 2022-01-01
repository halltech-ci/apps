# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomSaleInherit(http.Controller):
#     @http.route('/hta_custom_sale_inherit/hta_custom_sale_inherit/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_sale_inherit/hta_custom_sale_inherit/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_sale_inherit.listing', {
#             'root': '/hta_custom_sale_inherit/hta_custom_sale_inherit',
#             'objects': http.request.env['hta_custom_sale_inherit.hta_custom_sale_inherit'].search([]),
#         })

#     @http.route('/hta_custom_sale_inherit/hta_custom_sale_inherit/objects/<model("hta_custom_sale_inherit.hta_custom_sale_inherit"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_sale_inherit.object', {
#             'object': obj
#         })
