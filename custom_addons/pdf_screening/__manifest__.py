{
    'name': 'PDF Screening',
    'version': '1.0',
    'summary': 'Custom PDF Screening Module',
    'description': 'A custom module for screening PDF files in Odoo.',
    'category': 'Custom',
    'depends': ['base'],
    'data': [
        'views/views.xml',
        'security/security.xml',
    ],
    'application': True,
}
