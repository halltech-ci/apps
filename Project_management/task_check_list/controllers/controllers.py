# -*- coding: utf-8 -*-
# from odoo import http


# class TaskCheckList(http.Controller):
#     @http.route('/task_check_list/task_check_list/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/task_check_list/task_check_list/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('task_check_list.listing', {
#             'root': '/task_check_list/task_check_list',
#             'objects': http.request.env['task_check_list.task_check_list'].search([]),
#         })

#     @http.route('/task_check_list/task_check_list/objects/<model("task_check_list.task_check_list"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('task_check_list.object', {
#             'object': obj
#         })
