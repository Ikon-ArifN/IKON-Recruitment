from odoo import models, fields

class ModelJob(models.Model):
    _inherit = "hr.job"

    position_code = fields.Char(string='Position Code', size=20)