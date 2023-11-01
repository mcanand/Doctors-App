from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import date


class ChitPartner(models.Model):
    _name = 'chit.partner'
    _rec_name = 'name'

    name = fields.Char(compute="_compute_name")

    @api.depends('partner_id', 'name')
    def _compute_name(self):
        for rec in self:
            rec.name = rec.partner_id.name

    partner_id = fields.Many2one('res.partner')
    chit_fund_id = fields.Many2one('chit.fund')
    chit_month_id = fields.Many2one('chit.month')
    chit_state = fields.Selection([('won', 'Won'), ('pending', 'Pending')])
    chit_won_date = fields.Date()
    chit_won_month = fields.Integer()
    won_amount = fields.Float()
    deduction = fields.Float()
    company_id = fields.Many2one('res.company', compute="_compute_company")
    chit_partner_month_due_ids = fields.One2many('chit.partner.month.due',
                                                 'chit_partner_id')
    total_payment_due = fields.Float()
    has_payment_due = fields.Boolean()







    # @api.depends('chit_partner_month_due_ids', 'total_payment_due',
    #              'has_payment_due')
    # def _compute_total_payment_due(self):
    #     for rec in self:
    #         if rec.chit_partner_month_due_ids:
    #             # val = lambda x:x.state == 'pending',rec.chit_partner_month_due_ids.mapped('due_amount')
    #             total_due = 0
    #             for val in rec.chit_partner_month_due_ids:
    #                 if val.state == 'pending':
    #                     total_due += val.due_amount
    #             # total_due = sum(rec.chit_partner_month_due_ids.mapped('due_amount'))
    #             rec.total_payment_due = total_due
    #             rec.has_payment_due = True
    #         else:
    #             rec.total_payment_due = 0
    #             rec.has_payment_due = False
    def update_payment_due(self):
        if self.chit_partner_month_due_ids:
            total_due = 0
            for val in self.chit_partner_month_due_ids:
                if val.state == 'pending':
                    total_due += val.due_amount
            if total_due > 0:
                self.total_payment_due = total_due
                self.has_payment_due = True
            else:
                self.total_payment_due = 0
                self.has_payment_due = False

    @api.depends('company_id')
    def _compute_company(self):
        for rec in self:
            rec.company_id = self.env.company.id

    @api.model_create_multi
    def create(self, vals):
        chit_fund = self.env['chit.fund']
        for rec in vals:
            if rec.get('chit_fund_id') and rec.get('partner_id'):
                chit_fund = chit_fund.search(
                    [('id', '=', rec.get('chit_fund_id'))])
                members = [x.partner_id.id for x in chit_fund.chit_partner_ids]
                if rec.get('partner_id') in members:
                    raise ValidationError(_(self.env['res.partner'].search(
                        [('id', '=', rec.get(
                            'partner_id'))]).name + " Already exist in the list"))
                if len(members) == chit_fund.count:
                    raise ValidationError(_("You have added all the members"))
            rec['chit_state'] = 'pending'
        res = super(ChitPartner, self).create(vals)
        return res

    # TODO check the create same as write need to write


    def write(self, vals):
        for rec in self:
            if 'chit_fund_id' in vals or 'partner_id' in vals:
                chit_fund = self.env['chit.fund'].search([('id', '=', vals.get('chit_fund_id', rec.chit_fund_id.id))])
                members = [x.partner_id.id for x in chit_fund.chit_partner_ids]
                if rec.get('partner_id') in members:
                    raise ValidationError(_(self.env['res.partner'].search(
                        [('id', '=', rec.get(
                            'partner_id'))]).name + " Already exist in the list"))
                if len(members) == chit_fund.count:
                    raise ValidationError(_("You have added all the members"))
        vals['chit_state'] = 'pending'
        res = super(ChitPartner, self).write(vals)
        return res

    def action_mark_won(self):
        chit_month = self.env['chit.month']
        domain = [('chit_fund_id', '=', self.chit_fund_id.id),
                  ('chit_partner_id', '=', self.id)]
        chit_month_val = chit_month.search(domain)
        if self.chit_fund_id and chit_month_val:
            vals = self.prepare_chit_partner_vals(chit_month_val)
            vals['chit_state'] = 'won'
            self.write(vals)
            self.chit_fund_id.write({
                'balance_amount': chit_month_val.balance_amount,
                'current_month': chit_month_val.month + 1
            })
            self.chit_fund_id.create_chit_month_with_partner()

    def prepare_chit_partner_vals(self, chit_month_val):
        vals = {
            'chit_won_date': date.today(),
            'chit_won_month': chit_month_val.month,
            'chit_month_id': chit_month_val.id,
            'won_amount': chit_month_val.won_amount,
            'deduction': chit_month_val.deducted_amount,
        }
        return vals

    def action_mark_pending(self):
        self.chit_state = 'pending'

