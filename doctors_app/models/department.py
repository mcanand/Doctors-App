from odoo import api, fields, models


class Department(models.Model):
    _inherit = 'hr.department'


    image = fields.Binary(string='Image')
