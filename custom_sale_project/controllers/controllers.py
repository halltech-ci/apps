# -*- coding: utf-8 -*-
# from odoo import http


# class CustomSaleProject(http.Controller):
#     @http.route('/custom_sale_project/custom_sale_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_sale_project/custom_sale_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_sale_project.listing', {
#             'root': '/custom_sale_project/custom_sale_project',
#             'objects': http.request.env['custom_sale_project.custom_sale_project'].search([]),
#         })

#     @http.route('/custom_sale_project/custom_sale_project/objects/<model("custom_sale_project.custom_sale_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_sale_project.object', {
#             'object': obj
#         })
