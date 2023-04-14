# -*- coding: utf-8 -*-
{
    'name': "Promotion Letter",

    'summary': """
        Create Promotion for selected Employee""",

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
    'depends': ['base','hr','warning_letter'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/letter_report_template.xml',
        'views/views.xml',
        
    ],

}
