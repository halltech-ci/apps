# -*- coding: utf-8 -*-
# from odoo import http


# class HtaCustomProject(http.Controller):
#     @http.route('/hta_custom_project/hta_custom_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_custom_project/hta_custom_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_custom_project.listing', {
#             'root': '/hta_custom_project/hta_custom_project',
#             'objects': http.request.env['hta_custom_project.hta_custom_project'].search([]),
#         })

#     @http.route('/hta_custom_project/hta_custom_project/objects/<model("hta_custom_project.hta_custom_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_custom_project.object', {
#             'object': obj
#         })
