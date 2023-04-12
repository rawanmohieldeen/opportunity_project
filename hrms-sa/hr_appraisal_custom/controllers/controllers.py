# -*- coding: utf-8 -*-
# from odoo import http


# class HrAppraisalCustom(http.Controller):
#     @http.route('/hr_appraisal_custom/hr_appraisal_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_appraisal_custom/hr_appraisal_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_appraisal_custom.listing', {
#             'root': '/hr_appraisal_custom/hr_appraisal_custom',
#             'objects': http.request.env['hr_appraisal_custom.hr_appraisal_custom'].search([]),
#         })

#     @http.route('/hr_appraisal_custom/hr_appraisal_custom/objects/<model("hr_appraisal_custom.hr_appraisal_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_appraisal_custom.object', {
#             'object': obj
#         })
