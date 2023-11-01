from odoo import models, fields


class PayMonthDue(models.TransientModel):
    _name = 'pay.due'

    chit_partner_month_due_ids = fields.Many2many('chit.partner.month.due')

    def action_done(self):
        print('x')