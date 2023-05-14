# -*- coding: utf-8 -*-
{
    'name': "HR End Of Service",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','hr_custom','hr_payroll_community','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/hr_exit_interview_template.xml',
        'report/final_settelment_report.xml',
        'report/final_payment_report.xml',
        'views/reports.xml',
        'views/hr_exit_factors.xml',
        'views/hr_exit_interview.xml',
        'views/service_certificate.xml',
        'views/final_settelment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
