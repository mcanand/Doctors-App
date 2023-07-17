from odoo import models, fields

class SignupChoice(models.Model):
    _name = 'signup.choice'
    _description = 'Signup Choice'

    choice = fields.Selection([
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ], string='Signup Choice', required=True)
