from odoo import fields, models, api
from datetime import date


class ChitPartnerMonthDue(models.Model):
    _name = 'chit.partner.month.due'

    chit_month_partner_id = fields.Many2one('chit.month.partner')
    chit_month_id = fields.Many2one('chit.month')
    chit_partner_id = fields.Many2one('chit.partner')
    due_amount = fields.Float()
    state = fields.Selection([('pending', 'Pending'), ('paid', 'Paid')],
                             default='pending')
    paid_on = fields.Date()
    paid_month = fields.Integer()

    # pay_due_id = fields.Many2one('pay.due',ondelete='cascade')

    def action_mark_paid(self):
        self.state = 'paid'
        self.paid_on = date.today()
        active_id = self.env.context.get('active_id')
        if active_id:
            chit_month_partner = self.env['chit.month.partner'].browse(int(active_id))
            self.paid_month = chit_month_partner.month
        self.chit_partner_id.update_payment_due()
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

    def action_mark_not_paid(self):
        self.state = 'pending'
        self.paid_on = ''
        self.paid_month = 0
        self.chit_partner_id.update_payment_due()
        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }


