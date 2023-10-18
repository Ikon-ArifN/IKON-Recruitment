
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import logging

logger = logging.getLogger(__name__)

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


    def website_form_input_filter(self, request, values):
        
        
            
        # screening_records = self.env['ir.attachment'].sudo().search([
        #     ('user_id', '=', ids.user_id),
        #     ('mimetype', '=', 'application/pdf')
        # ])
        
        # logger.info(screening_records.name)



        if 'partner_name' in values:
            applicant_job = self.env['hr.job'].sudo().search([('id', '=', values['job_id'])]).name if 'job_id' in values else False
            name = '%s - %s' % (values['partner_name'], applicant_job) if applicant_job else _("%s's Application", values['partner_name'])
            values.setdefault('name', name)
        if values.get('job_id'):
            job = self.env['hr.job'].browse(values.get('job_id'))
            if not job.sudo().website_published:
                raise UserError(_("You cannot apply for this job."))
            stage = self.env['hr.recruitment.stage'].sudo().search([
                ('fold', '=', False),
                '|', ('job_ids', '=', False), ('job_ids', '=', values['job_id']),
            ], order='sequence asc', limit=1)
            if stage:
                values['stage_id'] = stage.id
                
    
      
        return values
    
    