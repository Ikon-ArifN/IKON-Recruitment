from odoo import models, fields, api
import base64
import io
from pdfminer.high_level import extract_text
import logging

_logger = logging.getLogger(__name__)

class HrJobMatching(models.Model):
    _name = 'hr.job.matching'
    _description = 'Job Matching'

    score = fields.Float('Score')
    user_id = fields.Many2one('res.users', 'User')
    job_id = fields.Many2one('hr.job', 'Job')

    # Add other fields or methods as needed

    @api.model
    def perform_matching(self, job_id):
        # Langkah 1: Cari attachment dengan res_model 'hr.applicant' dan job_id tertentu
        attachment_records = self.env['ir.attachment'].search([
            ('res_model', '=', 'hr.applicant'),
            ('mimetype', '=', 'application/pdf'),
            ('res_id', '=', job_id)
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

                # Langkah 2: Ambil keterampilan yang dibutuhkan dari hr.job.skill_ids
                job = self.env['hr.job'].search([('id', '=', job_id)], limit=1)
                required_skills = job.skill_ids.mapped('name')

                for skill in required_skills:
                    if skill.lower() in extracted_text.lower():
                        matching_skills.append(skill)
                        matching_skill_names.append(skill)

                if matching_skills:
                    total_score = (len(matching_skills) / len(required_skills)) * 100
                    total_score = min(total_score, 100)

                    # Langkah 3: Simpan skor, job_id, dan user_id pada objek hr.job.matching
                    job_matching = self.env['hr.job.matching'].search([('job_id', '=', job_id)], limit=1)
                    if job_matching:
                        job_matching.write({
                            'score': total_score,
                            'job_id': job_id,
                            'user_id': applicant.user_id.id,
                        })

    def extract_text_from_attachment(self, attachment):
        pdf_data = base64.b64decode(attachment.datas)
        with io.BytesIO(pdf_data) as pdf_file:
            text = extract_text(pdf_file)
        return text
