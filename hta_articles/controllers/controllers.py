# -*- coding: utf-8 -*-
# from odoo import http


# class HtaArticles(http.Controller):
#     @http.route('/hta_articles/hta_articles/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hta_articles/hta_articles/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hta_articles.listing', {
#             'root': '/hta_articles/hta_articles',
#             'objects': http.request.env['hta_articles.hta_articles'].search([]),
#         })

#     @http.route('/hta_articles/hta_articles/objects/<model("hta_articles.hta_articles"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hta_articles.object', {
#             'object': obj
#         })
