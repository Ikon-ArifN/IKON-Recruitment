from odoo import models, fields

class ModelDepartment(models.Model):
    _inherit = "hr.department"

    department_code = fields.Char(string='Department Code', size=20)