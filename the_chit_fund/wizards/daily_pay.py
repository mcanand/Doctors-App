from odoo import api, fields, models

class PaymentWizard(models.TransientModel):
    _name = 'payment.daily'


    payment_amount = fields.Float(string='Payment Amount', required=True)
    is_daily = fields.Boolean(string='Daily Payment', default=True)
    chit_month_partner_id = fields.Many2one('chit.month.partner', string="Chit Month Partner")

    def confirm_payment(self):
        for payment in self:
            chit_month_partner = payment.chit_month_partner_id

            # Reduce the payable field in chit.month.partner
            chit_month_partner.payable -= payment.payment_amount

            # Get the related chit.partner.month record
            chit_partner_month = chit_month_partner.chit_month_id

            # Reduce the payable field in chit.partner.month
            chit_partner_month.payable -= payment.payment_amount

        return {'type': 'ir.actions.act_window_close'}
