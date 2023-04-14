# -*- coding: utf-8 -*-
# from odoo import http


# class BusinessRequest(http.Controller):
#     @http.route('/business_request/business_request', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/business_request/business_request/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('business_request.listing', {
#             'root': '/business_request/business_request',
#             'objects': http.request.env['business_request.business_request'].search([]),
#         })

#     @http.route('/business_request/business_request/objects/<model("business_request.business_request"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('business_request.object', {
#             'object': obj
#         })
