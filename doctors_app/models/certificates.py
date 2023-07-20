from odoo import fields, models


class Certificates(models.Model):
    _name = 'doctor.certificate'
    _description = 'Doctor Certificates'

    name = fields.Char(string='Name')
    attachment = fields.Binary(string='Attachment')
    mimetype = fields.Char(string='MIME Type')
