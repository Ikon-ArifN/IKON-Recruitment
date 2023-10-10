from odoo import models, fields, api, exceptions
from werkzeug.security import generate_password_hash


from odoo.http import request

class UserModel(models.Model):
    _inherit = 'res.users'

    name = fields.Char(String='Nama user', required=True, track_visibility='always')
    email = fields.Char(String='Email user', required=True, help='Email User')
    login = fields.Char(String='Login or Username user', required=True, help='Username user')
    password = fields.Char(String='Password User', required=True, help='Password user')
    active = fields.Boolean(String='Active status', default=False, help='User Active')

