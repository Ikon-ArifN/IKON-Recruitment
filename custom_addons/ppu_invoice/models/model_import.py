from odoo import models, fields, api

class ImportDataWizard(models.TransientModel):
    _name = 'import.data.wizard'
    _description = 'Import Data Wizard'

    # Define any fields needed for the import process
    data_file = fields.Binary(string='Data File', required=True)
    file_name = fields.Char(string='File Name')

    # Method to handle the import action
    def perform_import(self):
        # Implement your import logic here
        # This method will be called when the user clicks on the "Import" button
        pass
