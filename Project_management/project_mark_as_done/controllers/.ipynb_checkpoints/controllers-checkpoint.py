# -*- coding: utf-8 -*-
# from odoo import http


# class ProjectMarkAsDone(http.Controller):
#     @http.route('/project_mark_as_done/project_mark_as_done/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_mark_as_done/project_mark_as_done/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_mark_as_done.listing', {
#             'root': '/project_mark_as_done/project_mark_as_done',
#             'objects': http.request.env['project_mark_as_done.project_mark_as_done'].search([]),
#         })

#     @http.route('/project_mark_as_done/project_mark_as_done/objects/<model("project_mark_as_done.project_mark_as_done"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_mark_as_done.object', {
#             'object': obj
#         })
