{
    'name': 'Disciplinary Action',
    'version': '1.0',
    'author': 'Mogtaba Mohammed',
    'license': 'LGPL-3',
    'category': 'HR',
    'depends': [
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/hr_offence.xml',
        'views/offence_report.xml',
        # 'wizard/hr_offence_report_wizard.xml',
        # 'report/report.xml',
        # 'report/report_offence.xml',
    ],
    
    'auto_install': False,
    'application': False,
    
}