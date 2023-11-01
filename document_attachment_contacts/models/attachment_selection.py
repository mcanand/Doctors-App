from odoo import models, fields
from odoo.exceptions import ValidationError

class AttachmentSelection(models.Model):
    _name = 'contact.attachment.selection'
    _description = 'Select Attachments'

    name = fields.Char(string='Document Name')
    certificates = fields.One2many('ir.attachment','res_id', string='Certificates')
    partner_id = fields.Many2one('res.partner', string='Certifi')









