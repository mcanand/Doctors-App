from odoo import models, fields, api, _
import random
from odoo.exceptions import ValidationError


class UpdateWinner(models.TransientModel):
    _name = 'update.winner'

    chit_partner_ids = fields.Many2many('chit.partner', readonly=True)
    chit_partner_id = fields.Many2one('chit.partner',
                                      domain="[('id','in',chit_partner_ids)]")



    def action_pick_one(self):
        object = self.env[self.env.context.get('active_model')].search(
            [('id', '=', self.env.context.get('active_id'))])
        if self.chit_partner_ids:
            chit_partner = random.choice(self.chit_partner_ids).id
            object.chit_partner_id = chit_partner

    def action_done(self):
        if self.chit_partner_id:
            object = self.env[self.env.context.get('active_model')].search(
                [('id', '=', self.env.context.get('active_id'))])
            object.chit_partner_id = self.chit_partner_id.id
        else:
            raise ValidationError(
                _("Please Select a Member OR Click Pick Random Button"))
