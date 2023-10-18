from odoo import models, fields, api
import logging

logger = logging.getLogger(__name__)

class CustomWebsite(models.Model):
    _inherit = 'website'

    # Define fields if needed

    # Add your custom method
    @api.model
    def insert_attachment(self, model, id_record, files):
        logger.info(files)
        
