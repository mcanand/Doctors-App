from odoo import fields, models, api, _
import razorpay

class PaymentProviderInherit(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('razorpay', "razor pay")],
        ondelete={'razorpay': 'set default'})

    razorpay_endpoint = fields.Char(string="End point",
                                    required_if_code='razorpay')
    razorpay_api_key = fields.Char(string="API key",
                                   required_if_code='razorpay')
    razorpay_secret_key = fields.Char(string="Secret Key",
                                      required_if_code='razorpay')

