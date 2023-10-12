from odoo import models, fields

class SkillTag(models.Model):
    _name = 'skill.tag'
    _description = 'Skill Tags'

    name = fields.Char(string='Tag Name', required=True)

class SkillSet(models.Model):
    _name = 'skill.set'
    _description = 'Skill Set'

    name = fields.Char(string='Name', required=True)
    skills = fields.Many2many('skill.tag', string='Skills', help="Select or add skills")

    # Your other fields and methods here
