# -*- coding: utf-8 -*-
from openerp import http

# class InspectionTech(http.Controller):
#     @http.route('/inspection_tech/inspection_tech/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inspection_tech/inspection_tech/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('inspection_tech.listing', {
#             'root': '/inspection_tech/inspection_tech',
#             'objects': http.request.env['inspection_tech.inspection_tech'].search([]),
#         })

#     @http.route('/inspection_tech/inspection_tech/objects/<model("inspection_tech.inspection_tech"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inspection_tech.object', {
#             'object': obj
#         })