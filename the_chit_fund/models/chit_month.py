from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import inflect


class ChitMonth(models.Model):
    _name = 'chit.month'

    name = fields.Char(compute="_compute_name")
    month = fields.Integer(readonly=True)
    won_amount = fields.Float(readonly=True)
    payable = fields.Float(readonly=True)
    total_amount = fields.Float(readonly=True)
    balance_amount = fields.Float(readonly=True)
    bid_amount = fields.Float(compute="_compute_bid_amount")
    starting_bid_amount = fields.Float(readonly=True)
    chit_commission_amount = fields.Float(readonly=True)
    deducted_amount = fields.Float(readonly=True)
    chit_fund_id = fields.Many2one('chit.fund')
    chit_partner_id = fields.Many2one('chit.partner',
                                      domain="[('id','in',chit_partner_ids)]",
                                      states={'done': [('readonly', True)]})
    chit_partner_ids = fields.Many2many('chit.partner',
                                        compute="_compute_chit_partner_ids")
    total_deduction = fields.Integer(string="Total Deduction (in %)",
                                     readonly=True)
    chit_month_partner_ids = fields.One2many('chit.month.partner',
                                             'chit_month_id')
    chit_month_bid_ids = fields.One2many('chit.month.bid', 'chit_month_id')
    state = fields.Selection(
        [('draft', 'Draft'), ('live', 'Live'), ('done', 'Closed')],
        default='draft')
    active_month = fields.Boolean()
    lucky_draw_till = fields.Integer(
        string="Lucky Draw Till (How Many Months)")
    draw_type = fields.Selection([('lucky', 'Lucky Draw'), ('bid', 'Bidding')],
                                 compute="_compute_lucky_draw_bidding")

    @api.depends('bid_amount')
    def _compute_bid_amount(self):
        for rec in self:
            if rec.chit_month_bid_ids:
                rec.bid_amount = min(
                    rec.chit_month_bid_ids.mapped('bid_amount'))
            else:
                rec.bid_amount = 0

    @api.depends('name', 'month', 'chit_partner_ids', 'chit_partner_id')
    def _compute_chit_partner_ids(self):
        for val in self:
            chit_partner_ids = []
            pending_members = [x.id for x in filter(lambda x: x.chit_state == 'pending',
                                       val.chit_fund_id.chit_partner_ids)]
            for rec in self.chit_month_partner_ids:
                if rec.chit_partner_id.id in pending_members:
                    if not rec.has_payment_due:
                        chit_partner_ids.append(rec.chit_partner_id.id)
            val.chit_partner_ids = chit_partner_ids

    @api.depends('lucky_draw_till', 'draw_type')
    def _compute_lucky_draw_bidding(self):
        for rec in self:
            if rec.month > rec.lucky_draw_till:
                rec.draw_type = 'bid'
            else:
                if rec.lucky_draw_till > 0:
                    rec.draw_type = 'lucky'
                else:
                    rec.draw_type = ''

    @api.depends('name', 'month')
    def _compute_name(self):
        p = inflect.engine()
        for rec in self:
            rec.name = rec.chit_fund_id.name + " Chit" + " " + p.ordinal(
                rec.month) + " Month Details"

    def action_make_live(self):
        self.state = 'live'

    def action_close_this_month(self):
        self.pre_check_paid()
        if self.draw_type == 'bid' and self.bid_amount == 0:
            raise ValidationError(
                _("There is no Bid amount Found for Current Month Please Add it in Members Bids"))
        if self.chit_partner_id:
            self.write({'balance_amount': self.calculate_balance_amount(),
                        'won_amount': self.calculate_won_amount(),
                        'deducted_amount': self.calculate_deduct_amount()})
            self.chit_partner_id.action_mark_won()
            self.write({'state': 'done'})
        else:
            raise ValidationError(
                _("You Must Provide This Month Chit Winner To The Details"))

    def action_update_winner(self):
        self.pre_check_paid()
        if self.draw_type == 'bid':
            lowest_bidders = self.get_lowest_bidder()
            if not lowest_bidders:
                raise ValidationError(
                    _("There is no Bidders Found for Current Month Please Add"))
            if len(lowest_bidders) > 1:
                chit_partner_ids = [x.chit_partner_id.id for x in
                                    lowest_bidders]
                return self.open_update_winner_wizard(chit_partner_ids)
            else:
                for rec in lowest_bidders:
                    self.chit_partner_id = rec.chit_partner_id.id
        else:
            paid_chit_partner_ids = [x.chit_partner_id.id for x in self.chit_month_partner_ids if x.state == 'paid']

            return self.open_update_winner_wizard(paid_chit_partner_ids)
            # chit_partner_ids = [x.id for x in
            #                     self.chit_partner_ids]
            # return self.open_update_winner_wizard(chit_partner_ids)

    def open_update_winner_wizard(self,chit_partner_ids):
        wizard = self.env['update.winner'].create(
            {'chit_partner_ids': chit_partner_ids})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'update.winner',
            'view_mode': 'form',
            'res_id': wizard.id,
            'target': 'new',
        }

    def calculate_balance_amount(self):
        """calculate balance by total_deduction - company_chit_commission_amount"""
        chit_fund = self.chit_fund_id
        total_amount = self.total_amount
        total_deduction = self.calculate_deduct_amount()
        chit_commission = chit_fund.chit_commission
        company_comm_amount = (chit_commission * total_amount) / 100
        balance = total_deduction - company_comm_amount
        if self.draw_type == 'bid':
            balance = self.calculate_deduct_amount()
        return balance

    def calculate_deduct_amount(self):
        """calculate deduction if lucky draw:
                    get total deduction percentage that is chit_commission(%) + other_deduction(%) and
                    calculate the percentage from total amount of chit"""
        if self.draw_type == 'lucky':
            total_amount = self.total_amount
            amount = (self.total_deduction * total_amount) / 100
            return amount
        elif self.draw_type == 'bid':
            amount = self.starting_bid_amount - self.bid_amount
            return amount

    def calculate_won_amount(self):
        """won amount is calculated by (total_amount - deduct_amount)- due"""
        if self.draw_type == 'lucky':
            won_amount = self.total_amount - self.calculate_deduct_amount()
            won_amount = won_amount - self.chit_partner_id.total_payment_due
            return won_amount
        else:
            won_amount = self.bid_amount
            won_amount = won_amount - self.chit_partner_id.total_payment_due
            return won_amount

    def get_lowest_bidder(self):
        """get the lowest bidder in the list"""
        if self.chit_month_bid_ids:
            amount = min(self.chit_month_bid_ids.mapped('bid_amount'))
            low_bid_ids = list(filter(lambda x: x.bid_amount == amount,
                                      self.chit_month_bid_ids))
            return low_bid_ids

    def pre_check_paid(self):
        """check all members are paid in chit_month_partner_ids"""
        if self.chit_month_partner_ids:
            unpaid_members = list(filter(lambda x: x.state == 'unpaid',
                                         self.chit_month_partner_ids))
            if unpaid_members:
                raise ValidationError(
                    _("Members not paid their amount please check\n" + '\n'.join(
                        [x.chit_partner_id.partner_id.name for x in
                         unpaid_members])))
            else:
                return True

    def unlink(self):
        for rec in self:
            if rec.state in ['draft', 'live', 'done']:
                raise ValidationError(_("You cant delete Month Entry"))
        res = super(ChitMonth, self).unlink()
        return res
