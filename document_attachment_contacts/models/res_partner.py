from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    certificate_ids = fields.One2many('contact.attachment.selection','partner_id',string="attachment")



    def action_open_documents(self):
     return {
        'name': 'Add Document',
        'type': 'ir.actions.act_window',
        'res_model': 'contact.attachment.selection',
        'view_mode': 'form',
        'view_type': 'form',
        'view_id': self.env.ref('document_attachment_contacts.view_attachment_selection_form').id,
        'target': 'new',
        'context': {
            'default_partner_id': self.id,
        }
    }