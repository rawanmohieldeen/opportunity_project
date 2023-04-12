# -*- coding: utf-8 -*-
# from odoo import http


# class HrRecruitmentTerms(http.Controller):
#     @http.route('/hr_recruitment_terms/hr_recruitment_terms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_recruitment_terms/hr_recruitment_terms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_recruitment_terms.listing', {
#             'root': '/hr_recruitment_terms/hr_recruitment_terms',
#             'objects': http.request.env['hr_recruitment_terms.hr_recruitment_terms'].search([]),
#         })

#     @http.route('/hr_recruitment_terms/hr_recruitment_terms/objects/<model("hr_recruitment_terms.hr_recruitment_terms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_recruitment_terms.object', {
#             'object': obj
#         })
