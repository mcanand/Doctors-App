from odoo import models, fields, api

class ChitEnquiry(models.Model):
    _name = 'chit.enquiry'
    _description = 'Chit Fund Enquiry'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    message = fields.Text(string='Message')
    confirm = fields.Boolean(string='Confirm')
    chit_fund_id = fields.Many2one('chit.fund', string='Chit Fund')






