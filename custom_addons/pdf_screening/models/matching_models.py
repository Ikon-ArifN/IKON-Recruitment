from odoo import models, fields, api
from fuzzywuzzy import fuzz
import logging

logger = logging.getLogger(__name__)

class MatchingResume(models.Model):
    _name = 'matching.resume'
    _description = 'Matching Resume'

    name = fields.Char(string='Name')
    skill_tag_ids = fields.Many2many('skill.tag', string='Skill Tags')
    pdf_screening_ids = fields.Many2many('pdf.screening', string='PDF Screenings')
    result = fields.Text(string='Matching Result', readonly=True)
    persons = fields.Integer(compute="_compute_person_count")
    person_ids = fields.Many2many('pdf.screening', string='Persons', compute='_compute_persons')

    @api.depends('person_ids')
    def _compute_persons(self):
        matching_name = self.name  # Assuming 'person_ids' is a Many2one field
        logger.info(matching_name)
        # logger.info(matching_name)
        # domain = [('matching_name', '=', matching_name)]
        persons = self.env['pdf.screening'].search([('matching_name', '=', matching_name)])
        
        self.person_ids = [(6, 0, persons.ids)]

    def open_persons_form(self):
        return {
        'type': 'ir.actions.act_window',
        'name': 'Matching Persons',
        'res_model': 'pdf.screening',
        'view_mode': 'tree,form',
        'view_type': 'form',
        'domain': [('id', 'in', self.person_ids.ids),],
        'target': 'current',
        'context': {'order': 'scores desc'},
        }
    # Method to perform the matching process
    def perform_matching(self):
        result = {}
        pdf_screening_model = self.env['pdf.screening']
        screening_records = pdf_screening_model.search([])

        required_skills = set(self.skill_tag_ids.mapped('name'))

        for screening in screening_records:
            extracted_text = screening.extracted_text
            candidate_name = screening.name

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

                pdf_screening_record = pdf_screening_model.search([('name', '=', candidate_name)], limit=1)
                if pdf_screening_record:
                    pdf_screening_record.write({'scores': total_score, 'status': 'sudah dimatching', 'matching_name': self.name})

    # Update the result in the matching.resume record
        self.write({'result': result})
