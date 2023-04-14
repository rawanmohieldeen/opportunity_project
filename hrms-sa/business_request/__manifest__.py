# -*- coding: utf-8 -*-
{
    'name': "Business Travel Request Form",

    'summary': """
        Form and report of Business Travel Request Form""",

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
    'depends': ['hr','hr_employee_updation'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'report/request_report_template.xml',
        'report/expense_claim_report.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
   
}
