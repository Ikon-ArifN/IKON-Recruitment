{
    'name': 'PPU Invoice',
    'version': '1.0',
    'category': 'Sales',
    'author': 'IKON',
    'depends': ['base', 'sale'],
    'data': [
        'views/ppu_invoice_template.xml',
        # 'controllers/controllers.xml',
        'security/ir.model.access.csv',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
