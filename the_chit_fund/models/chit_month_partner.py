from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ChitMonthPartner(models.Model):
    _name = 'chit.month.partner'

    payable = fields.Float()
    chit_month_id = fields.Many2one('chit.month')
    chit_partner_id = fields.Many2one('chit.partner')
    month = fields.Integer()
    state = fields.Selection([('unpaid', 'Not Paid'),
                              ('paid', 'Paid'),
                              ('later', 'Pay Next Month')],
                             default='unpaid')
    has_payment_due = fields.Boolean()
    total_payment_due = fields.Float(compute="_compute_total_payment_due")

    @api.depends('state', 'total_payment_due', 'has_payment_due')
    def _compute_total_payment_due(self):
        for rec in self:
            if rec.chit_partner_id.chit_partner_month_due_ids:
                total_due = 0
                for val in rec.chit_partner_id.chit_partner_month_due_ids:
                    if val.state == 'pending':
                        total_due += val.due_amount
                rec.total_payment_due = total_due
            else:
                rec.total_payment_due = 0

    def action_mark_paid(self):
        # view_id = self.env.ref('the_chit_fund.view_payment_wizard_form1').id
        # action_id = self.env.ref('the_chit_fund.action_all_slots').id
        # return {
        #     'name': 'Booked Slots',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'payment.daily',
        #     'view_mode': 'form',
        #     'views': [(view_id, 'form')],
        #     'target': 'new',
        #     'action': action_id,
        # }

        self.check_parent_state()
        self.state = 'paid'
        self.update_pay_later_dues()

    def action_mark_not_paid(self):
        self.check_parent_state()
        self.state = 'unpaid'
        self.update_pay_later_dues()

    def action_mark_pay_later(self):
        self.check_is_eligible_pay_later()
        self.check_parent_state()
        self.state = 'later'
        self.update_pay_later_dues()
        message = "Payment Dues Are Updated For Member", self.chit_partner_id.name
        not_type = 'success'
        return self.return_dispaly_notification(message, not_type)

    def return_dispaly_notification(self, message, not_type):
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'target': 'new',
            'params': {
                'message': _(message),
                'type': not_type,
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }

    def check_is_eligible_pay_later(self):
        if self.chit_partner_id.chit_state != 'pending':
            raise ValidationError(_("This member already won a Chit"))

    def update_pay_later_dues(self):
        if self.state == 'later':
            self.chit_partner_id.chit_partner_month_due_ids.create({
                'chit_month_partner_id': self.id,
                'chit_month_id': self.chit_month_id.id,
                'chit_partner_id': self.chit_partner_id.id,
                'due_amount': self.payable
            })
        else:
            due = self.env['chit.partner.month.due'].search(
                [('chit_month_partner_id', '=', self.id)])
            due.unlink()
        self.chit_partner_id.update_payment_due()

    def check_parent_state(self):
        """check chit month state is live or not"""
        if not self.chit_month_id.state == 'live':
            raise ValidationError(_("Go live to change payment details"))

    def action_pay_due(self):
        wizard = self.env['pay.due'].create(
            {
                'chit_partner_month_due_ids': self.chit_partner_id.chit_partner_month_due_ids})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pay.due',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }

    # def update_payment_due(self):
    #     """update the payment due"""
    #     if self.chit_partner_id.chit_partner_month_due_ids:
    #         # val = lambda x:x.state == 'pending',rec.chit_partner_month_due_ids.mapped('due_amount')
    #         total_due = 0
    #         for val in self.chit_partner_id.chit_partner_month_due_ids:
    #             if val.state == 'pending':
    #                 total_due += val.due_amount
    #         # total_due = sum(rec.chit_partner_month_due_ids.mapped('due_amount'))
    #         self.write({'total_payment_due': total_due})
    #     else:
    #         self.write({'total_payment_due': 0})








