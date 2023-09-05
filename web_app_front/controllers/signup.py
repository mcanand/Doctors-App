import logging
import werkzeug
from werkzeug.urls import url_encode

from odoo import http, tools, _
from odoo.addons.auth_signup.models.res_users import SignupError

from odoo.exceptions import UserError
from odoo.http import request
from odoo.addons.auth_signup.controllers.main import AuthSignupHome as BaseAuthSignupHome

class AuthSignupHome(BaseAuthSignupHome):

    @http.route('/web/signup', type='http', auth='public', website=True, sitemap=False)
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()
        if kw.get('signup_enabled') and kw.get('signup_enabled') == 'True':
            qcontext.update({'signup_enabled': True})

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                qcontext.update({'signup_enabled': False})
                self.do_signup(qcontext)
                # Send an account creation confirmation email
                User = request.env['res.users']
                user_sudo = User.sudo().search(
                    User._get_login_domain(qcontext.get('login')), order=User._get_login_order(), limit=1
                )
                template = request.env.ref('auth_signup.mail_template_user_signup_account_created',
                                           raise_if_not_found=False)
                if user_sudo and template:
                    template.sudo().send_mail(user_sudo.id, force_send=True)
                return self.web_login(*args, **kw)
            except UserError as e:
                qcontext['error'] = e.args[0]
            except (SignupError, AssertionError) as e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error"] = _("Another user is already registered using this email address.")
                else:
                    # _logger.error("%s", e)
                    qcontext['error'] = _("Could not create a new account.")

        elif 'signup_email' in qcontext:
            user = request.env['res.users'].sudo().search(
                [('email', '=', qcontext.get('signup_email')), ('state', '!=', 'new')], limit=1)
            if user:
                return request.redirect('/web/login?%s' % url_encode({'login': user.login, 'redirect': '/web'}))

        response = request.render('auth_signup.signup', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    def _prepare_signup_values(self, qcontext):
        # Call the parent class's _prepare_signup_values method
        values = super(AuthSignupHome, self)._prepare_signup_values(qcontext)
        values['categry_id'] = 'patient'  # Add your custom value here
        return values


class SignupPageControllerAdd(http.Controller):
    @http.route('/loading/page', type='http', auth='public',website=True)
    def signup_page(self):
        return http.request.render('web_app_front.signup_page_template')

    @http.route('/doctor/account/view', type='http', auth='public', website=True)
    def doctor_account_view(self):
        return http.request.render('web_app_front.doctor_account_view')

