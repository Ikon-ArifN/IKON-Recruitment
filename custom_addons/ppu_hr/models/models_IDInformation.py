from odoo import models, fields

class IDInformation(models.Model):
    _name = 'employee.id_information'
    _description = 'ID Information'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    ID_Number = fields.Char(string='ID Number')
    ID_Type = fields.Char(string='ID Type')
    Effective_Date = fields.Date(string='Effective Date')
    Expired_Date = fields.Date(string='Expired Date')
