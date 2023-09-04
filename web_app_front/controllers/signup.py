from odoo import http

class SignupPageExtraControllerAdd(http.Controller):
    @http.route('/loading/page', type='http', auth='public',website=True)
    def signup_page(self):
        return http.request.render('web_app_front.signup_page_template')