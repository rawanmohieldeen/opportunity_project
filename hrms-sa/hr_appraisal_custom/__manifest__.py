# -*- coding: utf-8 -*-
{
    'name': "Probation Appraisal Form and Confirmation Letter",

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
    'depends': ['base','hr','hr_contract','hr_employee_updation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/templates.xml',
        'data/data.xml',
        'report/probation_appraisal_template.xml',
        'report/confirmation_letter.xml',   
        'views/views.xml',
    ],

}
