# -*- coding: utf-8 -*-
# from odoo import http


# class HtaSaleProject(http.Controller):
#     @http.route('/hta_sale_project/hta_sale_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_sale_project/hta_sale_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_sale_project.listing', {
#             'root': '/hta_sale_project/hta_sale_project',
#             'objects': http.request.env['hta_sale_project.hta_sale_project'].search([]),
#         })

#     @http.route('/hta_sale_project/hta_sale_project/objects/<model("hta_sale_project.hta_sale_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_sale_project.object', {
#             'object': obj
#         })
