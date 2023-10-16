from odoo import models, fields

class HrApplicant(models.Model):
    _inherit = "hr.applicant"
    
    indeed_profile = fields.Char(string="Indeed Profile")
    glints_profile = fields.Char(string="Glints Profile")
    nik = fields.Char(string="NIK")
    gender = fields.Selection([
            ('male', 'Male'),
            ('female', 'Female')
        ],string="Gender")
    dob = fields.Date(string="Date of Birth")
    address = fields.Char(string="Address")
    martial_status = fields.Selection([
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
        ], string="Martial Status")
    religion = fields.Selection([
            ('islamic', 'Islam'),
            ('christian', 'Christian'),
            ('hindu', 'Hindu'),
            ('buddha', 'Buddha'),
            ('catholic', 'Catholic'),
            ('khonghucu', 'Khonghucu'),
            ('not say', 'Rather Not Say')
        ], string="Religion")
    last_salary = fields.Integer(string='Last Salary')
    fresh_grad = fields.Boolean(string="Fresh Graduate")
    
    experience_ids = fields.One2many('hr.experience', 'applicant_id' ,string="Experience")
    