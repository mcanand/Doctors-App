from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date
from num2words import num2words
from dateutil.relativedelta import relativedelta


class ChitFunds(models.Model):
    _name = "chit.fund"
    _inherit = ['mail.thread']
    _description = 'Chit fund management'

    name = fields.Char(string="Chit Fund Name", required=True,
                       states={'in_progress': [('readonly', True)],
                               'done': [('readonly', True)],
                               'close': [('readonly', True)]},
                       tracking=True)
    company_id = fields.Many2one('res.company', readonly=True)
    type = fields.Selection([('regular', 'Regular')], required=True)
    span = fields.Integer(string="Total Span of Chit fund (in Months)",
                          required=True,
                          states={'in_progress': [('readonly', True)],
                                  'done': [('readonly', True)],
                                  'close': [('readonly', True)]})
    count = fields.Integer(string="Total Number of people",
                           compute="calculate_count", store=True)
    amount = fields.Float(string="Total Chit Amount", tracking=True,
                          states={'in_progress': [('readonly', True)],
                                  'done': [('readonly', True)],
                                  'close': [('readonly', True)]})
    balance_amount = fields.Float(readonly=True,
                                  string="prev Month Balance Amount")
    amount_words = fields.Char(compute="_compute_amount_words")
    amount_payable = fields.Float(string="Amount Payable (/person)",
                                  readonly=True, digits=[16, 2],
                                  compute="_compute_amount_payable")
    amount_payable_words = fields.Char(compute="_compute_amount_words")
    start_date = fields.Date(string="Start Date", required=True,
                             states={'in_progress': [('readonly', True)],
                                     'done': [('readonly', True)],
                                     'close': [('readonly', True)]})
    end_date = fields.Date(string="End Date", compute="_compute_end_date")
    current_month_date = fields.Date(string="Current Month Date", compute="_compute_current_month_date")
    chit_partner_ids = fields.One2many('chit.partner', 'chit_fund_id', states={
        'in_progress': [('readonly', True)], 'done': [('readonly', True)],
        'close': [('readonly', True)]}, tracking=True)
    chit_month_ids = fields.One2many('chit.month', 'chit_fund_id',readonly=True,
                                     tracking=True, states={
            'in_progress': [('readonly', True)], 'done': [('readonly', True)],
            'close': [('readonly', True)]})
    current_month = fields.Integer(string="Current Chit Month", default=1,
                                   tracking=True,
                                   states={'in_progress': [('readonly', True)],
                                           'done': [('readonly', True)],
                                           'close': [('readonly', True)]})
    currency_id = fields.Many2one('res.currency', compute="_compute_currency")
    state = fields.Selection(
        [('draft', 'Waiting'), ('in_progress', 'Running'), ('done', 'Done'),
         ('close', 'Canceled')], tracking=True, group_expand='_expand_groups',
        default='draft')
    members_count = fields.Integer(compute="_compute_members_count")
    chit_commission = fields.Integer(string="Chit Commission (in %)",
                                     required=True)
    other_deduction = fields.Integer(
        string="Other Deductions (in %) Except chit Commission", required=True,
        states={'in_progress': [('readonly', True)],
                'done': [('readonly', True)],
                'close': [('readonly', True)]})
    draw_type = fields.Selection([('lucky', 'Lucky Draw'), ('bid', 'Bidding')],
                                 compute="_compute_lucky_draw_bidding",
                                 tracking=True)
    lucky_draw_till = fields.Integer(
        string="Lucky Draw Till (How Many Months)",
        required=True,
        states={'in_progress': [('readonly', True)],
                'done': [('readonly', True)],
                'close': [('readonly', True)]})




    @api.onchange('start_date')
    def change_start_date(self):
        if self.start_date:
            if self.start_date < date.today():
                raise ValidationError(_("Date should be greater than today's date"))

    @api.depends('start_date','current_month_date')
    def _compute_current_month_date(self):
        for rec in self:
            if rec.start_date:
                rec.current_month_date = rec.start_date + relativedelta(months=rec.current_month)
            else:
                rec.current_month_date = ''

    @api.depends('start_date', 'end_date')
    def _compute_end_date(self):
        for rec in self:
            if rec.start_date:
                rec.end_date = rec.start_date + relativedelta(months=rec.span)
            else:
                rec.end_date = ''

    @api.model
    def _expand_groups(self, states, domain, order):
        return ['draft', 'in_progress', 'done', 'close']

    @api.depends('amount_payable', 'balance_amount', 'span', 'amount')
    def _compute_amount_payable(self):
        for rec in self:
            if rec.amount > 0 and rec.span > 0:
                if rec.balance_amount > 0:
                    rec.amount_payable = (
                                                 rec.amount - rec.balance_amount) / rec.span
                else:
                    rec.amount_payable = rec.amount / rec.span
            else:
                rec.amount_payable = 0

    @api.depends('lucky_draw_till', 'draw_type')
    def _compute_lucky_draw_bidding(self):
        for rec in self:
            if rec.current_month > rec.lucky_draw_till:
                rec.draw_type = 'bid'
            else:
                if rec.lucky_draw_till > 0:
                    rec.draw_type = 'lucky'
                else:
                    rec.draw_type = ''

    @api.onchange('lucky_draw_till')
    def onchange_lucky_draw_till(self):
        if self.lucky_draw_till and self.span and self.lucky_draw_till > self.span:
            raise ValidationError(
                _("Value must be less than Total Span of Chit Fund"))
        if self.lucky_draw_till > 0:
            self.draw_type = 'lucky'

    @api.onchange('other_deduction')
    def onchange_other_deduction(self):
        if self.other_deduction and self.other_deduction > 100:
            raise ValidationError(
                _("Value must be in Percentage \nThe value should be less than 100"))

    @api.depends('members_count')
    def _compute_members_count(self):
        for rec in self:
            rec.members_count = len(rec.chit_partner_ids)

    @api.depends('currency_id', 'amount', 'amount_payable')
    def _compute_amount_words(self):
        for rec in self:
            if rec.amount and rec.currency_id:
                rec.amount_words = self.convert_amount_to_text(rec.amount,
                                                               rec.currency_id)
                rec.amount_payable_words = self.convert_amount_to_text(
                    rec.amount_payable, rec.currency_id)
            else:
                rec.amount_words = ''
                rec.amount_payable_words = ''

    @api.depends('company_id')
    def _compute_currency(self):
        for rec in self:
            rec.currency_id = rec.company_id.currency_id.id

    @api.depends('span')
    def calculate_count(self):
        for rec in self:
            if rec.span:
                rec.count = rec.span

    @api.model_create_multi
    def create(self, vals_list):
        for vals_list in vals_list:
            if vals_list.get('amount') > 0 and vals_list.get(
                    'span') > 0 and vals_list.get('chit_commission') > 0:
                vals_list['amount_payable'] = round(
                    (vals_list.get('amount') / vals_list.get('span')), 2)
            else:
                if vals_list.get('amount') == 0:
                    raise ValidationError(
                        _("Total Chit Amount Value Must Be Greater Than Zero(0)"))
                elif vals_list.get('chit_commission') == 0:
                    raise ValidationError(_("Chit Commission Cant be Zero"))
                elif vals_list.get('span') == 0:
                    raise ValidationError(
                        _("Total Span of Chit Value Must Be Greater Than Zero(0)"))
            vals_list['company_id'] = self.env.company.id
        res = super(ChitFunds, self).create(vals_list)
        return res

    def convert_amount_to_text(self, amount, currency_id):
        if len(str(amount)) > 10:
            if amount > 0 and currency_id:
                first = int(str(amount).split('.')[0])
                second = int(str(amount).split('.')[1])
                if len(str(second)) > 9:
                    amount = round(amount, 2)
                    second = int(str(amount).split('.')[1])
                text1 = num2words(first,
                                  lang='en').title() if first > 0 else ''
                text2 = num2words(second,
                                  lang='en').title() if second > 0 else ''
                if text1 and text2:
                    return text1 + ' ' + currency_id.currency_unit_label + ' And ' + text2 + ' ' + currency_id.currency_subunit_label
                elif text1:
                    return text1 + ' ' + currency_id.currency_unit_label
                elif text2:
                    return text2 + ' ' + currency_id.currency_subunit_label
        else:
            return currency_id.amount_to_text(amount)

    def action_start(self):
        if date.today() < self.start_date:
            raise ValidationError(_("Wait For the date to start"))
        if len(self.chit_partner_ids) == 0:
            raise ValidationError(
                _("Add " + str(self.count) + " Members To The Chit"))
        if len(self.chit_partner_ids) == self.count:
            self.create_chit_month_details()
            self.write({'state': 'in_progress'})
        else:
            raise ValidationError(_("Number of members required is " + str(
                self.count) + " \nThere is " + str(len(
                self.chit_partner_ids)) + " Members"))

    # def action_draft(self):
    #     self.write({'state': 'draft'})

    def action_close(self):
        self.write({'state': 'close'})

    def action_current_month(self):
        chit_month = self.env['chit.month'].search(
            [('id', 'in', [x.id for x in self.chit_month_ids]),
             ('month', '=', self.current_month)], limit=1)
        if chit_month:
            return {'name': 'This Month',
                    'type': 'ir.actions.act_window',
                    'res_model': 'chit.month',
                    'view_mode': 'form',
                    'res_id': chit_month.id,
                    'domain': [
                        ('id', 'in', [x.id for x in self.chit_month_ids]),
                        ('month', '=', self.current_month)]
                    }
        elif not chit_month and self.state != 'done':
            raise ValidationError(
                _("Start Your Chit To See Current Month Details"))
        elif not chit_month and self.state == 'done':
            raise ValidationError(
                _("This Chit has been completed"))

    def action_all_months(self):
        chit_months = self.env['chit.month'].search(
            [('id', 'in', [x.id for x in self.chit_month_ids])])
        if chit_months:
            return {'name': 'This Month',
                    'type': 'ir.actions.act_window',
                    'res_model': 'chit.month',
                    'view_mode': 'tree,form',
                    'context': {'create': False},
                    'domain': [
                        ('id', 'in', [x.id for x in self.chit_month_ids])]
                    }
        else:
            raise ValidationError(
                _("Start Your Chit To See All Month Details"))

    def action_members(self):
        return {'name': _('Members'),
                'type': 'ir.actions.act_window',
                'res_model': 'res.partner',
                'view_mode': 'kanban,tree,form',
                'target': 'current',
                'context': {'create': False},
                'domain': [('id', 'in',
                            [x.partner_id.id for x in self.chit_partner_ids])]
                }

    def create_chit_month_details(self):
        chit_month = self.create_chit_month_with_partner()
        # print(chit_month)

    def create_chit_month_with_partner(self):
        if self.current_month <= self.span:
            chit_month_model = self.env['chit.month']
            active_month = chit_month_model.search(
                [('chit_fund_id', '=', self.id), ('active_month', '=', True)])
            if active_month:
                active_month.write({'active_month': False})
            chit_month_val = {
                'month': self.current_month,
                'payable': self.amount_payable,
                'chit_fund_id': self.id,
                'state': 'draft',
                'active_month': True,
                'lucky_draw_till': self.lucky_draw_till,
                'total_amount': self.amount,
                'total_deduction': self.get_total_deduction_in_perc(),
                'starting_bid_amount': self.calculate_bid_amount(),
                'chit_commission_amount': self.get_amount_after_chit_commission()
            }
            lines = []
            for line in self.chit_partner_ids:
                vals = {
                    'month': self.current_month,
                    'state': 'unpaid',
                    'payable': self.amount_payable,
                    'chit_partner_id': line.id,
                    'has_payment_due': line.has_payment_due,
                    'total_payment_due': line.total_payment_due
                }
                lines.append((0, 0, vals))
            chit_month_val.update({'chit_month_partner_ids': lines})
            chit_month = self.env['chit.month'].create(chit_month_val)
            return chit_month
        else:
            self.write({'state': 'done'})

    def get_total_deduction_in_perc(self):
        """get the total deduction in percentage"""
        if self.draw_type == 'lucky':
            return self.other_deduction + self.chit_commission
        elif self.draw_type == 'bid':
            # TODO
            return 1

    def calculate_bid_amount(self):
        """calculate bid starting bid amount"""
        if self.current_month > self.lucky_draw_till:
            bid_amount = self.amount - self.get_amount_after_chit_commission()
            return bid_amount
        else:
            return 0

    def get_amount_after_chit_commission(self):
        """get the amount after minusing chit commission eg:5%"""
        if self.chit_commission and self.amount:
            return (self.chit_commission * self.amount) / 100

    def unlink(self):
        for rec in self:
            if rec.state in ['in_progress', 'done']:
                raise ValidationError(
                    _("You cant delete a chit that in Running or Done state"))
        res = super(ChitFunds, self).unlink()
        return res
