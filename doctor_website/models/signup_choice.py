from odoo import models, fields

class SignupChoice(models.Model):
    _name = 'doctor_website.signup_choice'
    _description = 'Signup Choice'

    choice = fields.Selection([
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ], string='Signup Choice', required=True)
