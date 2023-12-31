from odoo import models, fields, api, Command
import razorpay


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    doctor_id = fields.Many2one('res.partner', string='Doctor')
    partner_ids = fields.Many2many('res.partner', string="Patients")
    razor_pay_id = fields.Char()


    def get_rz_pay_provider(self):
        """get payment provider"""
        provider = self.env['payment.provider']
        provider = provider.search([('code', '=', 'razorpay')], limit=1)
        return provider

    def get_api_key(self):
        api_key = self.get_rz_pay_provider().razorpay_api_key
        return api_key if api_key else False

    def get_secret_key(self):
        secret_key = self.get_rz_pay_provider().razorpay_secret_key
        return secret_key if secret_key else False

    @api.model
    def get_base_url(self):
        return self.env['ir.config_parameter'].sudo().get_param('web.base.url')

    def create_razorpay_link(self, values):
        client = razorpay.Client(
            auth=(self.get_api_key(), self.get_secret_key()))
        vals = self.prepare_razor_pay_values(values)
        response = client.payment_link.create(vals)
        return response

    def prepare_razor_pay_values(self, values):
        vals = {
            "amount": values.get('amount') * 100,
            "currency": "INR",
            "accept_partial": False,
            "first_min_partial_amount": 0,
            "description": "Doctor Meeting Payment",
            "customer": {
                "name": values.get('name'),
                "email": values.get('email'),
                "contact": values.get('contact')
            },
            "notify": {
                "sms": True,
                "email": True,
                "Whatsapp": True
            },
            "reminder_enable": True,
            "options": {
                "checkout": {
                    "theme": {
                        "hide_topbar": True
                    },
                    "name": self.env.company.name,
                    "method": {
                        "netbanking": "1",
                        "card": "1",
                        "upi": "1",
                        "wallet": "0"
                    }
                }
            },
            "notes": {
                "policy_name": self.env.company.name
            },
            "callback_url": values.get('call_back_url'),
            "callback_method": "get"
        }
        return vals

    def create_invoice(self):
        out_invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'date': self.create_date.strftime('%Y-%m-%d'),
            'invoice_date': self.create_date.strftime('%Y-%m-%d'),
            'invoice_line_ids': [Command.create({
                'product_id': self.env.company.meeting_product_id.id,
                'price_unit': self.amount,
                'quantity': 1
            })]
        }])
        out_invoice.action_post()

        pmt_wizard = self.env['account.payment.register'].with_context(
            active_model='account.move', active_ids=out_invoice.ids).create({
            'amount': out_invoice.amount_total,
            'currency_id': out_invoice.currency_id.id,
            'payment_date': out_invoice.invoice_date,
        })
        pmt_wizard._create_payments()

    def create_bill(self):
        in_invoice = self.env['account.move'].create([{
            'move_type': 'in_invoice',
            'partner_id': self.doctor_id.id,
            'date': self.create_date.strftime('%Y-%m-%d'),
            'invoice_date': self.create_date.strftime('%Y-%m-%d'),
            'invoice_line_ids': [Command.create({
                'product_id': self.env.company.meeting_product_id.id,
                'price_unit': self.amount - ((self.env.company.deduction_percentage / 100) * self.amount),
                'quantity': 1
            })]
        }])
        in_invoice.action_post()
