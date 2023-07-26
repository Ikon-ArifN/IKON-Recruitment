from odoo import models, fields, api
from odoo.exceptions import  UserError, ValidationError
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class PpuInvoice(models.Model):
    _name = 'ppu_invoice.invoice'
    _description = 'PPU Invoice'

    # Fields
    id_number = fields.Char(string='Number', required=True)
    payment_type = fields.Selection([('transfer', 'Transfer'), ('cash', 'Cash')], string='Payment Type')
    price_net = fields.Float(string='Net Price')
    price_gross = fields.Float(string='Gross Price')
    currency = fields.Char(string='Currency')
    status = fields.Selection([('issued', 'Issued'), ('paid', 'Paid')], string='Status')
    seller_name = fields.Char(string='Seller Name')
    buyer_name = fields.Char(string='Buyer Name')
    issue_date = fields.Date(string='Issue Date')
    payment_to = fields.Date(string='Payment To')
    paid = fields.Float(string='Paid')
    tax_name_type = fields.Selection([
        ('vat', 'VAT'),
        ('translation_tax', 'Translation Tax')], string='Tax Name Type')

    def action_automate(self):
        api_url = 'https://dev.benemica.com/OpenAPI/api/Personal-Information/Read?Employee_ID_Number=1&Organization_Code=0436'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            logger.info(data)
        else:
            logger.info('Error:', response.status_code)

class IrModel(models.Model):
    _inherit = 'ir.model'

    @api.model_create_multi
    def create(self, vals_list):
        try:
            api_url = 'https://dev.benemica.com/OpenAPI/api/Personal-Information/Read?Employee_ID_Number=1&Organization_Code=0436'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                filtered_data = {key: value for key, value in data.items() if key not in ['Error_Mssg', 'Status_Request']}
                lowercase_data = {key.lower(): value for key, value in filtered_data.items()}
                keys = list(lowercase_data.keys())
                values = list(lowercase_data.values())

                logger.info("Keys: %s", keys)
                logger.info("Values: %s", values)
                for value in values:
                    logger.info("Data Type: %s", type(value))
            else:
                logger.error('Error: %s', response.status_code)

        except requests.exceptions.RequestException as e:
            logger.error('Error: %s', e)







