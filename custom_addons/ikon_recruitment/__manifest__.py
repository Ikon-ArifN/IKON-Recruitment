{
    'name': 'IKON Recruitment Module',
    'summary': """IKON Rec Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'images'  : [],
    'depends': ['base', 'website', 'website_hr_recruitment','hr_skills'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        # views
        'views/inherit/jobs_portal.xml',
        'views/inherit/footer_login.xml',
        'views/inherit/root_portal.xml',

        #Skills management
        'views/Skills Management/hr_job_view.xml',
        'views/Skills Management/custom_hr_applicant_kanban.xml',
        
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}