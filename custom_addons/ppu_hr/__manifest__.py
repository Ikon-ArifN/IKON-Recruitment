{
    'name': 'PPU HR',
    'summary': """PPU HR Module""",
    'version': '16.0',
    "author": "Ikon Developer",
    'company': 'Ikonsultan Inovatama',
    'website': 'https://www.ikonsultan.com',
    'category': 'Tools',
    'depends': ['base', 'hr_recruitment', 'hr_contract', 'website_hr_recruitment'],
    "external_dependencies": {"python3.9": ["graphene"]},
    'license': 'AGPL-3',
    'data': [
        # views
        'views/hr_employee_views.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    # 'post_init_hook': '_init_hook'
}
