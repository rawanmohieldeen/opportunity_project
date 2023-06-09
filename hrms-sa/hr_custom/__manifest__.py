# -*- coding: utf-8 -*-
{
    'name': "HR custom",
    'author': "azam mustafa mohamed",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'HR',
    'version': '16',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_contract','hr_recruitment','hr_payroll_community','warning_letter'],


    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'report/payroll_authorization_report.xml',
        'report/employee_application_report.xml',
        'report/manpower_planing_form_report.xml',
        'report/manpower_planing_report.xml',
        'report/policy_request_report.xml',
        'report/exit_checklist_template.xml',
        'report/salary_alignment_sheet_report.xml',
        'report/new_position_report.xml',
        'report/total_emp_cost_report.xml',
        'report/employee_application_report.xml',
        'report/joining_report_template.xml',
        'report/employment_offer_template.xml',
        'report/interview_evaluation_template.xml',
        'report/report.xml',
        'views/exit_checklist_view.xml',
        'views/joining_report_view.xml',
        'views/personnel_requisition.xml',
        'views/annual_manpower.xml',
        'views/policy_request.xml',
        'views/payroll_authorization.xml',
        'views/total_employee_cost.xml',
        'views/employment_application_form.xml',
        'views/interview_evaluation_sheet.xml',
        'views/salary_alignment_sheet.xml'

    ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}
