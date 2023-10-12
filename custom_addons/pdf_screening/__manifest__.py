{
    'name': 'Macthiing Resume',
    'version': '1.0',
    'summary': 'Matching and Screening Module',
    'description': 'A custom module for screening resume and matching skills files in Odoo.',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'views/resume_screening.xml',
        'views/skill_set.xml',
        'views/matching.xml',
        'views/menu.xml',
        'security/security.xml',
    ],
    'application': True,
}
