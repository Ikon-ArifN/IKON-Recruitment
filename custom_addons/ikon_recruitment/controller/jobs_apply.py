# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from werkzeug import urls
import logging
import io
import base64
from pdfminer.high_level import extract_text
logger = logging.getLogger(__name__)

from odoo import api, fields, models, _
from odoo.exceptions import UserError

# class RecruitmentSource(models.Model):
#     _inherit = 'hr.recruitment.source'

#     url = fields.Char(compute='_compute_url', string='Url Parameters')

#     @api.depends('source_id', 'source_id.name', 'job_id', 'job_id.company_id')
#     def _compute_url(self):
#         for source in self:
#             source.url = urls.url_join(source.job_id.get_base_url(), "%s?%s" % (
#                 source.job_id.website_url,
#                 urls.url_encode({
#                     'utm_campaign': self.env.ref('hr_recruitment.utm_campaign_job').name,
#                     'utm_medium': source.medium_id.name or self.env.ref('utm.utm_medium_website').name,
#                     'utm_source': source.source_id.name
#                 })
#     
#         ))


class Applicant(models.Model):

    _inherit = 'hr.applicant'

    skill_tag_ids = fields.Many2many('skill.tag', string='Skill Tags')
    scores = fields.Float(string='Percentage (%)')
    extracted_text = fields.Text(string='Extracted Text', readonly=True)


    def extract_text_from_attachment(self, attachment):
        pdf_data = base64.b64decode(attachment.datas)
        with io.BytesIO(pdf_data) as pdf_file:
            text = extract_text(pdf_file)
        return text
    
    def website_form_input_filter(self, request, values):
        logger.info(self.id)

        result = {}
        screening_records = self.env['ir.attachment'].sudo().search([
            ('res_model', '=', 'hr.applicant'),
            ('mimetype', '=', 'application/pdf')
        ])
        required_skills = set(self.skill_tag_ids.mapped('name'))

        for screening in screening_records:
            extracted_text = self.extract_text_from_attachment(screening)
            candidate_name = None

            # Retrieve the candidate's name from hr.applicant based on res_id
            if screening.res_id:
                applicant = self.env['hr.applicant'].sudo().browse(screening.res_id)
                candidate_name = applicant.partner_name

            if candidate_name:
                # Initialize variables to count matching skills and store skill names
                matching_skills = []
                matching_skill_names = []

                # Loop through required skills and check for matches in extracted_text
                for skill in required_skills:
                    if skill.lower() in extracted_text.lower():
                        matching_skills.append(skill)
                        matching_skill_names.append(skill)

                if matching_skills:
                    # Calculate the total score as a percentage
                    total_score = (len(matching_skills) / len(required_skills)) * 100

                    # Ensure the total score does not exceed 100%
                    total_score = min(total_score, 100)

                    result[candidate_name] = {"skills": matching_skill_names, "score": total_score}

                    # Update the hr.applicant record with the matching information
                    self.sudo().write({'scores': total_score, 'extracted_text': extracted_text})

        # Update the result in the matching.resume record
        self.write({'result': result})
        
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
