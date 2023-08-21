from odoo import http

class SignupPageControllerAdd(http.Controller):
    @http.route('/loading/page', type='http', auth='public',website=True)
    def signup_page(self):
        return http.request.render('web_app_front.signup_page_template')

    @http.route('/doctor/account/view', type='http', auth='public', website=True)
    def doctor_account_view(self):
        return http.request.render('web_app_front.doctor_account_view')