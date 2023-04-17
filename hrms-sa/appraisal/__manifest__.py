# -*- coding: utf-8 -*-
{
    'name': 'Appraisal',
    'author': 'Mogtaba Mohammed',
    'category': 'HR',
    'version': '16',

    'depends': ['base','hr','hr_custom'],


   
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'report/leave_app_report.xml',
        'report/report.xml',
        'report/appraisal_performance.xml',
        'report/appraisal_performance_counselling.xml',
        'views/appraisal_performance.xml',
        'views/appraisal_performance_counselling.xml',
        'views/leave_application_view.xml'

    ],
    "installable": True,
    "application": True,
    'license': 'LGPL-3',
}
