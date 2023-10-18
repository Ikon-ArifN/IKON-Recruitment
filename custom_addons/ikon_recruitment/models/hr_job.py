from odoo import models, fields, api
import base64
import io
from pdfminer.high_level import extract_text
import logging

_logger = logging.getLogger(__name__)

class HrJob(models.Model):
    _inherit = 'hr.job'

    skill_ids = fields.Many2many('hr.skill', string='Add Skill')
    matching_count = fields.Integer(string='Total Matching', compute='_compute_matching_count')

    def _compute_matching_count(self):
        matching_model = self.env['hr.job.matching']
        for job in self:
            job.matching_count = matching_model.search_count([('job_id', '=', job.id)])

    def perform_matching(self):
        matching_model = self.env['hr.job.matching']
        for job in self:
            attachment_records = self.env['ir.attachment'].search([
                ('res_model', '=', 'hr.applicant'),
                ('mimetype', '=', 'application/pdf')
            ])

            for attachment in attachment_records:
                extracted_text = self.extract_text_from_attachment(attachment)
                candidate_name = None

                if attachment.res_id:
                    applicant = self.env['hr.applicant'].sudo().browse(attachment.res_id)
                    candidate_name = applicant.partner_name

                if candidate_name:
                    matching_skills = []
                    matching_skill_names = []

                    required_skills = job.skill_ids.mapped('name')
                    

                    for skill in required_skills:
                        if skill.lower() in extracted_text.lower():
                            matching_skills.append(skill)
                            matching_skill_names.append(skill)
                    
                    if matching_skills:
                        total_score = (len(matching_skills) / len(required_skills)) * 100
                        total_score = min(total_score, 100)

                        
                        matching_record = matching_model.search([('job_id', '=', job.id), ('user_id', '=', applicant.user_id.id)], limit=1)
                        if not matching_record:
                            matching_model.create({
                            'score': total_score,
                            'job_id': job.id,
                            'user_id': applicant.user_id.id,
                            })
                        else:
                            matching_record.write({
                            'score': total_score,
                            })

    def extract_text_from_attachment(self, attachment):
        pdf_data = base64.b64decode(attachment.datas)
        with io.BytesIO(pdf_data) as pdf_file:
            text = extract_text(pdf_file)
        return text
