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
        # print(pdt_data)
        # {'razorpay_payment_id': 'pay_LLvIaGyHLOmLT1',
        #  'razorpay_payment_link_id': 'plink_LLvDyAPPEnOebO',
        #  'razorpay_payment_link_reference_id': '',
        #  'razorpay_payment_link_status': 'paid',
        #  'razorpay_signature': '1b39604b0bd3ff1378f94743627d15ab91fbe40338732ddb027120a06d02b3c6'}
        _logger.info("handling redirection from razorpay with data:\n%s",
                     pprint.pformat(pdt_data))
        """pt data link id will come"""
        if not pdt_data:
            pass
        if pdt_data:
            # ''plink_LLxjLZB18ybSkB''
            # if the payment status is paid
            domain = [('razor_pay_id', '=', pdt_data['razorpay_payment_link_id'])]
            details = request.env['payment.details'].sudo().search(domain,limit=1)
            if pdt_data.get('razorpay_payment_link_status') == 'paid':
                if details:
                    payment_renewal = request.env['payment.renewal']
                    exist_renewal = payment_renewal.sudo().search([('application_partner_id', '=', details.franchise_application_id.id),
                                                                   ('state','=','send')],limit=1)
                    if exist_renewal:
                        exist_renewal.set_paid()
                    # if franchise application not done then approve franchise
                    if details.franchise_application_id.status != 'done':
                        details.franchise_application_id.approve()
                    details.set_done()
                    # create renewal for next renewal date
                    renewal = payment_renewal.create_renewal_record(details)
                return request.redirect('/')
            if pdt_data.get('razorpay_payment_link_status') != 'paid':
                if details:
                    payment_renewal = request.env['payment.renewal']
                    exist_renewal = payment_renewal.sudo().search(
                        [('franchise_application_id', '=', details.franchise_application_id.id),
                         ('state', '=', 'send')], limit=1)
                    details.set_canceled()


        return request.redirect('/')
