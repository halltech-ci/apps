# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleTemplate(http.Controller):
#     @http.route('/hta_sale_template/hta_sale_template/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_template/hta_sale_template/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_template.listing', {
#             'root': '/hta_sale_template/hta_sale_template',
#             'objects': http.request.env['hta_sale_template.hta_sale_template'].search([]),
#         })

#     @http.route('/hta_sale_template/hta_sale_template/objects/<model("hta_sale_template.hta_sale_template"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_template.object', {
#             'object': obj
#         })
