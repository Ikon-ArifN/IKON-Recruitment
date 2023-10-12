from odoo import models, fields, api
# from fuzzywuzzy import fuzz
import logging

logger = logging.getLogger(__name__)



class MatchingResume(models.Model):
    _name = 'matching.resume'
    _description = 'Matching Resume'

    name = fields.Char(string='Name')
    skill_tag_ids = fields.Many2many('skill.tag', string='Skill Tags')
    pdf_screening_ids = fields.Many2many('pdf.screening', string='PDF Screenings')
    result = fields.Text(string='Matching Result', readonly=True)


    # Method to perform the matching process
    def perform_matching(self):
        result = {}
        pdf_screening_model = self.env['pdf.screening']
        screening_records = pdf_screening_model.search([])

        required_skills = set(self.skill_tag_ids.mapped('name'))

        for screening in screening_records:
            extracted_text = screening.extracted_text
            matching_skills = [skill for skill in required_skills if skill in extracted_text.lower()]

            if matching_skills:
                candidate_name = screening.name
                result[candidate_name] = matching_skills

    # Update the result in the matching.resume record
        self.write({'result': result})

