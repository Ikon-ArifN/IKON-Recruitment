from odoo import models, fields

class ModelContract(models.Model):
    _inherit = "hr.contract"

    date_of_hire = fields.Date(string='Date of Hire')
    join_date = fields.Date(string='Join Date')
    status_information_employee_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ],string='Status Information Employee Status')
    working_time_code = fields.Char(string='Working Time Code', size=20)
    division_code = fields.Char(string='Division Code', size=20)
    grade_code = fields.Char(string='Grade Code', size=20)
    cost_center = fields.Char(string='Cost Center', size=50)
    deputation = fields.Char(string='Deputation', size=50)
    contract_type = fields.Char(string='Contract Type', related='contract_type_id.name')
    position_code = fields.Char(related='job_id.position_code')
    department_code = fields.Char(related='department_id.department_code')
