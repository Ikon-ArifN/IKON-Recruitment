from odoo import models, fields, api
import requests
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Employee(models.Model):
    _inherit = 'hr.employee'

    Employee_ID_Number = fields.Char(string='Employee ID Number')
    Salutation = fields.Char(string='Salutation')
    Full_Name = fields.Char(string='Full Name')
    Place_of_Birth = fields.Char(string='Place of Birth')
    Date_of_Birth = fields.Date(string='Date of Birth')
    Mother_Maiden_Name = fields.Char(string='Mother Maiden Name')
    Age = fields.Integer(string='Age')
    Gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Gender')
    Religion = fields.Char(string='Religion')
    Blood_Type = fields.Char(string='Blood Type')
    Nationality = fields.Char(string='Nationality')
    Marital_Status = fields.Selection([
        ('single', 'SINGLE'),
        ('married', 'MARRIED'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed')
    ], string='Marital Status')
    Number_of_Children = fields.Integer(string='Number of Children')
    Last_Education = fields.Char(string='Last Education')
    BPJS_TK_NPP = fields.Char(string='BPJS TK NPP')
    BPJS_Healthcare_NPP = fields.Char(string='BPJS Healthcare NPP')
    List_ID_Information = fields.One2many('employee.id_information', 'employee_id', string='ID Information')
    List_Family_Information = fields.One2many('employee.family_information', 'employee_id', string='Family Information')
    Error_Mssg = fields.Char(string='Error Message')
    Status_Request = fields.Integer(string='Status Request')

    # def action_automate(self, vals_list):
    #         CustomEmployee.create(self, vals_list)



    @api.model_create_multi
    def create(self, vals_list):
        data_dict = vals_list[0]
        try:
            api_url = 'https://dev.benemica.com/OpenAPI/api/Personal-Information/Read?Employee_ID_Number=1&Organization_Code=0436'
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                datas = {
                    'company_id': data_dict['company_id'],
                    'employee_type': data_dict['employee_type'],
                    'name': data['Full_Name'],
                    'Full_Name': data['Full_Name'],
                    'Employee_ID_Number': data['Employee_ID_Number'],
                    'work_email': data_dict['work_email'],
                    'BPJS_Healthcare_NPP': data['BPJS_Healthcare_NPP'],
                    'Gender': data['Gender'].lower(),
                    'Date_of_Birth': data['Date_of_Birth'],
                    'Marital_Status': data['Marital_Status'].lower(),
                    'Last_Education': data['Last_Education'],
                    'BPJS_TK_NPP': data['BPJS_TK_NPP'],
                }
                employees = super().create(datas)
            else:
                logger.error('Error: %s', response.status_code)
        except requests.exceptions.RequestException as e:
            logger.error('Error: %s', e)

        return employees





class IDInformation(models.Model):
    _name = 'employee.id_information'
    _description = 'ID Information'

    employee_id = fields.Many2one('hr.employee', string='Employee')
    ID_Number = fields.Char(string='ID Number')
    ID_Type = fields.Char(string='ID Type')
    Effective_Date = fields.Date(string='Effective Date')
    Expired_Date = fields.Date(string='Expired Date')

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
