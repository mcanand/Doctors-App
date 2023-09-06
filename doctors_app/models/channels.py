from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class Channels(models.Model):
    _inherit = 'mail.channel'

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Channels, self).create(vals_list)
        for rec in res:
            rec.channel_member_ids[len(rec.channel_member_ids)-1].unlink()
        return res