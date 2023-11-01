from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ChitMonthBid(models.Model):
    _name = 'chit.month.bid'
    #
    chit_partner_id = fields.Many2one('chit.partner',
                                      domain="[('id','in',chit_partner_ids)]")
    chit_partner_ids = fields.Many2many('chit.partner',
                                        compute="_compute_chit_partner_ids")
    bid_amount = fields.Float()
    chit_month_id = fields.Many2one('chit.month')



    @api.depends('chit_month_id', 'chit_partner_ids', 'bid_amount',
                 'chit_partner_id')
    def _compute_chit_partner_ids(self):
        for val in self:
            chit_partner_ids = []
            pending_members = [x.id for x in
                                filter(lambda x: x.chit_state == 'pending' and not x.has_payment_due,
                                       val.chit_month_id.chit_fund_id.chit_partner_ids)]
            print(pending_members)
            # print(pending_members)
            for rec in self.chit_month_id.chit_month_partner_ids:
                if rec.chit_partner_id.id in pending_members:
                    if not rec.has_payment_due:
                        chit_partner_ids.append(rec.chit_partner_id.id)
            print('l',chit_partner_ids)
            val.chit_partner_ids = chit_partner_ids


    @api.onchange('bid_amount')
    def onchange_bid_amount(self):
        if self.bid_amount > self.chit_month_id.starting_bid_amount:
            raise ValidationError(_("The Bid Amount Must Lower Than " + str(
                self.chit_month_id.starting_bid_amount)))




