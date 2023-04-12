# -*- coding: utf-8 -*-
{
    'name': "hr_recruitment_terms",

    'category': 'Human Resources/Recruitment',
    'summary': 'Terms And Conditions for Recruitment Process and send the referance check form',

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_recruitment'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/terms_view.xml',
        'views/hr_recruitment_view.xml',
    ],

}
