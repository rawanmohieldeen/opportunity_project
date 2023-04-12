# -*- coding: utf-8 -*-
{
    'name': "hr_offence",

    'author': "huz.dark1@gmail.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '16.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_custom', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'report/offence_report.xml',
        'views/view_offence.xml',
    ],
    "installable": True,
    "application": False,
    'license': 'LGPL-3',
}
