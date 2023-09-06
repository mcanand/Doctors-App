from odoo import models, fields

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    doctor_id = fields.Many2one('res.partner', string='Doctor')

    # def create_transaction(self):
    #     tx = self.env['payment.transaction'].create({
    #         'amount': 100,
    #         'provider_id': provider.id,
    #         'currency_id': self.env.company.currency_id.id,
    #         'partner_id': portal_partner.id,
    #         'doctor_id':
    #     })