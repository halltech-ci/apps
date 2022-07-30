# -*- coding: utf-8 -*-
# from odoo import http


# class HtaProjectPhase(http.Controller):
#     @http.route('/hta_project_phase/hta_project_phase/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_project_phase/hta_project_phase/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_project_phase.listing', {
#             'root': '/hta_project_phase/hta_project_phase',
#             'objects': http.request.env['hta_project_phase.hta_project_phase'].search([]),
#         })

#     @http.route('/hta_project_phase/hta_project_phase/objects/<model("hta_project_phase.hta_project_phase"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_project_phase.object', {
#             'object': obj
#         })
