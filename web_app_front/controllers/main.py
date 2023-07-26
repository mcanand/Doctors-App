from odoo import http
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.home import Home as WebHome
import datetime


class MyHomepage(WebHome):
    @http.route()
    def view_appointments(self, **kwargs):
        user_partner_id = request.env.user.partner_id
        today = datetime.now().date()
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_ids', 'in', user_partner_id.ids),
            ('booking_button', '=', True),
            ('date', '=', today),
        ])

        booking_details = []

        for booking in bookings:
            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'from_time': booking.from_time,
                'date': booking.date,
                'meeting_link': booking.meeting_link,
            }
            print(booking_dict)
            booking_details.append(booking_dict)

        return http.request.render('web_app_front.homepage_inherit', {'appointments': booking_details})


class AppController(http.Controller):
    @http.route('/departments', type='http', auth='public', website=True)
    def doctor_departments(self):
        values = {}
        departments = request.env['hr.department'].sudo().search_read([])
        values['departments'] = departments
        return request.render('web_app_front.department', values)

    @http.route('/doctors', type='http', auth='public', website=True)
    def doctors_render(self):
        doctors = request.env['hr.employee'].search([])
        values = {'doctors': doctors}
        return request.render('web_app_front.doctors_view', values)

    # @http.route(['/get/doctors/<int:department_id>'], type='http', auth="public", website=True)
    # def get_doctors(self,department_id, **kw):
    #     print("ggggggg")
    #     department = request.env['hr.department'].sudo().browse(department_id)
    #     doctors = department.member_ids
    #     values = {
    #         'doctors': doctors,
    #     }
    #     print(values)
    #     return http.request.render('web_app_front.department_doctors', values)

    @http.route('/today/appointment', type='http', auth='user', website=True)
    def view_appointments(self, **kwargs):
        user_partner_id = request.env.user.partner_id
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_id', 'in', user_partner_id.ids),
            ('booking_button', '=', True)
        ])

        booking_details = []

        for booking in bookings:
            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'appoinment_time': booking.display_time_interval,
                'date': booking.date,
                'meeting_link': booking.meeting_link,
            }

            booking_details.append(booking_dict)

        return http.request.render('web_app_front.today_appointment', {'appointments': booking_details})


class CustomerPortalInherit(CustomerPortal):

    @route(['/my/account'], type='http', auth='user', website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                self.on_account_update(values, partner)
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'states': states,
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'partner_can_edit_vat': partner.can_edit_vat(),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        # response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        # response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response

    @route('/my/security', type='http', auth='user', website=True, methods=['GET', 'POST'])
    def security(self, **post):
        values = self._prepare_portal_layout_values()
        values['get_error'] = get_error
        values['allow_api_keys'] = bool(request.env['ir.config_parameter'].sudo().get_param('portal.allow_api_keys'))
        values['open_deactivate_modal'] = False

        if request.httprequest.method == 'POST':
            values.update(self._update_password(
                post['old'].strip(),
                post['new1'].strip(),
                post['new2'].strip()
            ))

        return request.render('portal.portal_my_security', values)


def get_error(e, path=''):
    """ Recursively dereferences `path` (a period-separated sequence of dict
    keys) in `e` (an error dict or value), returns the final resolution IIF it's
    an str, otherwise returns None
    """
    for k in (path.split('.') if path else []):
        if not isinstance(e, dict):
            return None
        e = e.get(k)

    return e if isinstance(e, str) else None
