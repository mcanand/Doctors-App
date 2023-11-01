from odoo import fields, models, api, _


class ResPartners(models.Model):
    _inherit = 'res.partner'

    chit_fund_ids = fields.Many2many('chit.fund',
                                     compute="_compute_chit_fund_ids")
    company_ids = fields.Many2many('res.company')

    @api.depends('chit_fund_ids')
    def _compute_chit_fund_ids(self):
        for rec in self:
            chit_partner_ids = self.env['chit.partner'].search(
                [('partner_id', '=', rec.id)])
            rec.chit_fund_ids = [x.chit_fund_id.id for x in chit_partner_ids]

    @api.model_create_multi
    def create(self, vals_list):
        for vals_list in vals_list:
            vals_list['company_id'] = self.env.company.id
        res = super(ResPartners, self).create(vals_list)
        return res

    def action_partner_chit_fund(self):
        return {
            'name': _('Chit Funds'),
            'view_mode': 'tree,form',
            'res_model': 'chit.fund',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [x.id for x in self.chit_fund_ids])],
            'context': {'create': False}
        }

    def action_partner_my_chit(self):
        return {
            'name': _('Chit Funds'),
            'view_mode': 'tree,form',
            'res_model': 'chit.fund',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.chit_fund_ids.ids)],
            'context': {'create': False}
        }

