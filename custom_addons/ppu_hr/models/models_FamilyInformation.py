from odoo import models, fields

class FamilyInformation(models.Model):
    _name = 'employee.family_information'
    _description = 'Family Information'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    Relationship = fields.Char(string='Relationship')
    Name = fields.Char(string='Name')
    No_KK = fields.Char(string='No KK')
    Date_of_Birth = fields.Date(string='Date of Birth')
    Gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
