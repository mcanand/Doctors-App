from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    deduction_percentage = fields.Integer(string='Reduction Percentage')
    product_id = fields.Many2one('product.product', string=' Product')
    meeting_id = fields.Many2one('product.product', string=' Meeting')
