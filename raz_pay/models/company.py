from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    deduction_percentage = fields.Integer(string='Deduction Percentage')
    meeting_product_id = fields.Many2one('product.product',
                                         string='Meeting Product')
    group_meeting_product_id = fields.Many2one('product.product',
                                               string='Group Meeting Product')
