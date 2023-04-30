# -*- coding: utf-8 -*-
# from odoo import http


# class EndOfService(http.Controller):
#     @http.route('/end_of_service/end_of_service', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/end_of_service/end_of_service/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('end_of_service.listing', {
#             'root': '/end_of_service/end_of_service',
#             'objects': http.request.env['end_of_service.end_of_service'].search([]),
#         })

#     @http.route('/end_of_service/end_of_service/objects/<model("end_of_service.end_of_service"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('end_of_service.object', {
#             'object': obj
#         })
