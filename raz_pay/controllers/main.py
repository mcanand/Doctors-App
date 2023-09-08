import logging
import pprint

import requests
from datetime import date, datetime, timedelta
from werkzeug import urls
from werkzeug.exceptions import Forbidden

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError
from odoo.http import request

_logger = logging.getLogger(__name__)


class CashFreeController(http.Controller):
    _return_url = '/payment/razorpay/return'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'],
        csrf=False,
        save_session=False
    )
    def cashfree_return_from_checkout(self, **pdt_data):
        _logger.info(
            "handling redirection from razorpay with data////////////:\n%s",
            pprint.pformat(pdt_data))
        """pt data link id will come"""
        if not pdt_data:
            print('pass')
            pass
        if pdt_data:
            print('inininininiin')
            # ''plink_LLxjLZB18ybSkB''
            # if the payment status is paid
            domain = [
                ('razor_pay_id', '=', pdt_data['razorpay_payment_link_id'])]
            transaction = request.env['payment.transaction'].sudo().search(
                domain, limit=1)
            if pdt_data.get('razorpay_payment_link_status') == 'paid':
                if transaction:
                    transaction.create_invoice()
                    transaction.create_bill()
                    transaction.write({'state': 'done'})
                    slot = request.env['doctor.time.slots'].search([('transaction_id', '=', transaction.id)])
                    partners = slot.partner_ids.ids + [transaction.partner_id.id]
                    slot.partner_ids = partners
                return request.redirect('/')
            if pdt_data.get('razorpay_payment_link_status') != 'paid':
                if transaction:
                    transaction.write({'state': 'cancel'})
        return request.redirect('/')
