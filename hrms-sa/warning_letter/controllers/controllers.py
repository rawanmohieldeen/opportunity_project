# -*- coding: utf-8 -*-
# from odoo import http


# class WarningLetter(http.Controller):
#     @http.route('/warning_letter/warning_letter', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warning_letter/warning_letter/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('warning_letter.listing', {
#             'root': '/warning_letter/warning_letter',
#             'objects': http.request.env['warning_letter.warning_letter'].search([]),
#         })

#     @http.route('/warning_letter/warning_letter/objects/<model("warning_letter.warning_letter"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warning_letter.object', {
#             'object': obj
#         })
