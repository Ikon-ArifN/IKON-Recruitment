from odoo import models, fields

class ModelContract(models.Model):
    _inherit = "hr.contract"

    date_of_hire = fields.Date(string='Date of Hire')
    join_date = fields.Date(string='Join Date')
    # contract_start_date = fields.Date(string='Contract Start Date')
    # contract_end_date = fields.Date(string='Contract End Date')