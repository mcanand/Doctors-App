from odoo import fields, models

class LabAttachment(models.Model):
    _name = 'lab.attachment'
    _description = 'Lab Attachment'

    name = fields.Char(string='Name')
    attachment = fields.Binary(string='Attachment')
    mimetype=fields.Char(string='mimetype')

