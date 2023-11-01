from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    chit_fund_ids = fields.Many2many('chit.fund',
                                     compute="_compute_chit_fund_ids")

    @api.depends('chit_fund_ids')
    def _compute_chit_fund_ids(self):
        for rec in self:
            chit_fund_ids = self.env['chit.fund'].search([('company_id', '=', rec.id)])
            rec.chit_fund_ids = [x.id for x in chit_fund_ids]

    def action_partner_chit_fund(self):
        return {
            'name': _('Chit Funds'),
            'view_mode': 'tree,form',
            'res_model': 'chit.fund',
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', [x.id for x in self.chit_fund_ids])],
            'context': {'create': False}
        }
