from odoo import models, fields

class ModelEmployee(models.Model):
    _inherit = 'hr.employee'

    # personal info
    employee_id_number = fields.Integer(string='Employee ID Number', required=True)
    salutation = fields.Char(string='Salutation', size=10)
    mother_maiden_name = fields.Char(string='Mother Maiden Name', size=100)
    religion = fields.Char(string='Religion', size=50)
    blood_type = fields.Char(string='Blood Type', size=5)
    number_of_children = fields.Integer(string='Number of Children')
    major = fields.Char(string='Major', size=100)
    bpjs_tk_npp = fields.Char(string='BPJS TK NPP', size=20)
    bpjs_healthcare_npp = fields.Char(string='BPJS Healthcare NPP', size=20)
    certificate = fields.Selection(selection_add=[
        ('sd', 'Elementary School'),
        ('smp', 'Middle School'),
        ('sma', 'High School'),
    ], string='Certificate Level', default='other', groups="hr.group_hr_user", tracking=True)

    # id information
    id_information_id_type = fields.Selection([
        ('ktp', 'KTP'),
        ('passport', 'Passport'),
    ], string="ID Information ID Type")
    id_information_id_number = fields.Char(string='ID Information ID Number', size=50)

    # tax info
    tax_id_number = fields.Char(string='Tax ID Number', size=50)
    tax_effective_date = fields.Date(string='Tax Effective Date')
    tax_revoke_date = fields.Date(string='Tax Revoke Date')
    tax_status_status = fields.Char(string='Tax Status Status', size=20)
    employee_tax_policy = fields.Char(string='Employee Tax Policy', size=100)
    previous_net_income = fields.Float(string='Previous Net Income', digits=(10, 2))
    previous_tax_paid = fields.Float(string='Previous Tax Paid', digits=(10, 2))

    # payslip
    payslip_distribution = fields.Selection([
        ('e-payslip', 'E-Payslip'),
        ('email', 'Email'),
    ], string="Payslip Distribution")
    user_name = fields.Char(string='User Name', size=50)
    password = fields.Char(string='Password', size=100)

    # address
    legal_address_address = fields.Char(string='Legal Address', size=200)
    legal_address_regency_city = fields.Char(string='Legal Address Regency/City', size=100)
    legal_address_district = fields.Char(string='Legal Address District', size=100)
    legal_address_village = fields.Char(string='Legal Address Village', size=100)
    legal_address_province = fields.Char(string='Legal Address Province', size=100)
    legal_address_country = fields.Many2one('res.country', 'Legal Address Country', groups="hr.group_hr_user", tracking=True)
    legal_address_post_code = fields.Char(string='Legal Address Post Code', size=20)
    permanent_address_is_the_same_as_legal_address = fields.Boolean(string='Permanent Address is the same as Legal Address')
    permanent_address_address = fields.Char(string='Permanent Address', size=200)
    permanent_address_regency_city = fields.Char(string='Permanent Address Regency/City', size=100)
    permanent_address_district = fields.Char(string='Permanent Address District', size=100)
    permanent_address_village = fields.Char(string='Permanent Address Village', size=100)
    permanent_address_province = fields.Char(string='Permanent Address Province', size=100)
    permanent_address_country = fields.Many2one('res.country', 'Permanent Address Country', groups="hr.group_hr_user", tracking=True)
    permanent_address_post_code = fields.Char(string='Permanent Address Post Code', size=20)
    mailing_address_is_the_same_as_legal_address = fields.Boolean(string='Mailing Address is the same as Legal Address')
    mailing_address_is_the_same_as_permanent_address = fields.Boolean(string='Mailing Address is the same as Permanent Address')
    mailing_address_address = fields.Char(string='Mailing Address', size=200)
    mailing_address_regency_city = fields.Char(string='Mailing Address Regency/City', size=100)
    mailing_address_district = fields.Char(string='Mailing Address District', size=100)
    mailing_address_village = fields.Char(string='Mailing Address Village', size=100)
    mailing_address_province = fields.Char(string='Mailing Address Province', size=100)
    mailing_address_country = fields.Many2one('res.country', 'Mailing Address Country', groups="hr.group_hr_user", tracking=True)
    mailing_address_post_code = fields.Char(string='Mailing Address Post Code', size=20)

    # email and phone info
    residential_phone_number = fields.Char(string='Residential Phone Number', size=20)
    office_phone_number = fields.Char(string='Office Phone Number', size=20)
    mobile_phone_number = fields.Char(string='Mobile Phone Number', size=20)
    corporate_email_address = fields.Char(string='Corporate Email Address', size=100)
    personal_email_address = fields.Char(string='Personal Email Address', size=100)

    # contract 
    date_of_hire = fields.Date(related='contract_id.date_of_hire', readonly=True)
    join_date = fields.Date(related='contract_id.join_date', readonly=True)
    contract_start_date = fields.Date(related='contract_id.date_start', readonly=True)
    contract_end_date = fields.Date(related='contract_id.date_end', readonly=True)
    status_information_employment_status = fields.Char(related='contract_id.contract_type', readonly=True)
    status_information_employee_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], related='contract_id.status_information_employee_status', readonly=False)
    end_date_of_probation = fields.Date(related='contract_id.trial_date_end', string='End Date of Probation', readonly=False)
    working_time_code = fields.Char(related='contract_id.working_time_code', readonly=False)
    position_code = fields.Char(related='contract_id.position_code')
    division_code = fields.Char(related='contract_id.division_code', readonly=False)
    department_code = fields.Char(related='contract_id.department_code')
    grade_code = fields.Char(related='contract_id.grade_code', readonly=False)
    cost_center = fields.Char(related='contract_id.cost_center', readonly=False)
    deputation = fields.Char(related='contract_id.deputation', readonly=False)

    # payment
    payment_type = fields.Char(string='Payment Type', size=50)
    payment_from_bank_account = fields.Char(string='Payment from Bank Account', size=50)
    employee_account_no = fields.Char(string='Employee Account No', size=50)
    employee_bank = fields.Char(string='Employee Bank', size=100)
    employee_bank_branch = fields.Char(string='Employee Bank Branch', size=100)
    employee_currency_code = fields.Char(string='Employee Currency Code', size=5)
    employee_account_name = fields.Char(string='Employee Account Name', size=100)
