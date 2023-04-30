{
    'name': 'HR Training Custom',
    'version': '1.0',
    'author': 'Mogtaba Mohammed',
    'license': 'LGPL-3',
    'category': 'HR',
    'depends': [
        'hr','hr_custom',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        # 'views/hr_exit_interview.xml',
        'views/hr_training_course.xml',
        'views/hr_training_plan.xml',
        'views/hr_training_course_report.xml',
        'views/hr_training_course_request.xml',
        'report/report.xml',
        'report/training_course.xml',
        'report/training_course_report.xml',
        'report/training_course_request_report.xml',
    ],
    
    'auto_install': False,
    'application': False,
    
}