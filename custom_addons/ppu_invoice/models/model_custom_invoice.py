from odoo import fields, models

class CustomInvoice(models.Model):
    _name = 'ppu_invoice_custom.model_custom_invoice'
    _description = 'Custom Invoice'

    # Add your custom fields here
    name = fields.Char(string='Invoice Name', required=True)
    amount_total = fields.Monetary(string='Total Amount')
    ...
