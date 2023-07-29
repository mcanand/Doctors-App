from odoo import http
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.web.controllers.home import Home
from datetime import datetime,date

class AppController(http.Controller):
    @http.route('/departments', type='http', auth='public', website=True)
    def doctor_departments(self):
        values = {}
        departments = request.env['hr.department'].sudo().search_read([])
        values['departments'] = departments
        return request.render('web_app_front.department', values)

    @http.route(['/get/doctors/<int:department_id>'], type='http', auth="public", website=True)
    def get_doctors(self, department_id, **kw):
        print("ggggggg")
        department = request.env['hr.department'].sudo().browse(department_id)
        doctors = department.member_ids
        values = {
            'doctors': doctors,
        }
        print(values)
        return http.request.render('web_app_front.department_doctors', values)

    @http.route('/today/appointment', type='http', auth='public', website=True)
    def view_appointments(self):
        user_partner_id = request.env.user.partner_id
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_ids', 'in', user_partner_id.ids),
            ('booking_button', '=', True),
            ('date' ,'=', datetime.now().strftime('%Y-%m-%d')),
        ])

        booking_details = []

        for booking in bookings:
            doctor_image_url = booking.doctor_id.image_1920 or ''
            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'appointment_time': booking.from_time,
                'appointment_end': booking.to_time,
                'doctor_image' : doctor_image_url,
                'department' : booking.doctor_id.department_id.name,
            }

            booking_details.append(booking_dict)
        return request.render('web_app_front.today_appointment', {'appointments': booking_details})




    @http.route('/prescription', type='http', auth='public', website=True)
    def prescription_user(self):
        user_partner_id = request.env.user.partner_id
        values = {}
        latest_prescription = request.env['doctor.patient.prescription'].sudo().search([
            ('partner_ids', 'in', [user_partner_id.id]),
        ])
        values['prescriptions'] = latest_prescription
        print(values)
        return request.render('web_app_front.prescription_list', values)

    @http.route(['/d/<int:id>'], type='http', auth='public', website=True)
    def get_prescription(self,id,**kw):
        values = {}
        latest_prescription = request.env['doctor.patient.prescription'].sudo().search([
            ('id', '=', id),
        ])
        values['prescription'] = latest_prescription
        print(values)
        return request.render('web_app_front.view_prescription',values)

    @route('/all/appointment', type='http', auth='public', website=True)
    def all_appointments(self, **kwargs):
        user_partner_id = request.env.user.partner_id
        today = date.today().strftime('%Y-%m-%d')

        bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_ids', 'in', user_partner_id.ids),
            ('booking_button', '=', True),
            ('date', '>=', today),
        ])

        previous_bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_ids', 'in', user_partner_id.ids),
            ('booking_button', '=', True),
            ('date', '<', today),
        ])

        booking_details = []
        previous_booking_details = []  # Initialize the list here

        for booking in bookings:
            doctor_image_url = booking.doctor_id.image_1920 or ''
            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'appointment_time': booking.from_time,
                'appointment_end': booking.to_time,
                'doctor_image': doctor_image_url,
                'id': booking.id,
                'department': booking.doctor_id.department_id.name,
            }

            booking_details.append(booking_dict)
            print(booking_details)

        for previous_booking in previous_bookings:
            doctor_image_url = previous_booking.doctor_id.image_1920 or ''
            previous_booking_dict = {
                'doctor_name': previous_booking.doctor_id.name,
                'appointment_time': previous_booking.from_time,
                'appointment_end': previous_booking.to_time,
                'doctor_image': doctor_image_url,
                'department': previous_booking.doctor_id.department_id.name,
            }

            previous_booking_details.append(previous_booking_dict)

        return http.request.render('web_app_front.all_appointment', {
            'appointments': booking_details,
            'previous_appointments': previous_booking_details,
        })

    @http.route(['/bookings/<int:id>'], type='http', auth='public', website=True)
    def get_bookings(self, id, **kw):
        values = {}
        latest_prescription = request.env['doctor.time.slots'].sudo().search([
            ('id', '=', id),
        ])
        values['booking'] = latest_prescription
        print(values)
        return request.render('web_app_front.booking_details', values)

    @http.route('/booking/time/edit', type='http', auth='user', website=True)
    def edit_booking_time(self, **kw):
        return http.request.render('web_app_front.edit_booking_time_template')

    @http.route('/booking/time/update', type='http', auth='public', website=True, method=['POST'])
    def update_booking_time(self, **kw):
        partner_id = request.env.user.partner_id
        partner = request.env.user.partner_id
        employee = request.env['hr.employee'].sudo().search([('partner_ids', '=', partner.id)], limit=1)
        date = kw.get('date')
        from_time = kw.get('from_time')
        to_time = kw.get('to_time')

        employee.write({
            'date': date,
            'time_from': from_time,
            'time_to': to_time,
        })

        return request.redirect('/my')

    @http.route('/today/appointment/doctor', type='http', auth='public', website=True)
    def view_appointments_doctor(self):
        doctor_id = request.env.user.employee_ids
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', doctor_id.id),
            ('booking_button', '=', True),
            ('date', '=', datetime.now().strftime('%Y-%m-%d')),
        ])

        booking_details = []

        for booking in bookings:
            booking_dict = {
                'patient_name': booking.partner_ids.name,
                'appointment_time': booking.from_time,
                'appointment_end': booking.to_time,
                'id': booking.id,
            }
            booking_details.append(booking_dict)

        return request.render('web_app_front.today_appointment_doctor', {'appointments': booking_details})

    @route('/all/appointment/doctor', type='http', auth='public', website=True)
    def all_appointments_doctor(self, **kwargs):
        doctor_id = request.env.user.employee_ids
        today = date.today().strftime('%Y-%m-%d')

        bookings = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', doctor_id.id),
            ('booking_button', '=', True),
            ('date', '>=', today),
        ])

        previous_bookings = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', doctor_id.id),
            ('booking_button', '=', True),
            ('date', '<', today),
        ])

        booking_details = []
        previous_booking_details = []

        for booking in bookings:
            booking_dict = {
                'patient_name': booking.partner_ids.name,
                'appointment_time': booking.from_time,
                'appointment_end': booking.to_time,
                'id': booking.id,
                'date' : booking.date,

            }

            booking_details.append(booking_dict)
            print(booking_details)

        for previous_booking in previous_bookings:
          previous_booking_dict = {
                'patient_name': previous_booking.doctor_id.name,
                'appointment_time': previous_booking.from_time,
                'appointment_end': previous_booking.to_time,
                'date' : previous_booking.date,

            }

          previous_booking_details.append(previous_booking_dict)

        return http.request.render('web_app_front.all_appointment_doctor', {
            'appointments': booking_details,
            'previous_appointments': previous_booking_details,
        })

    @http.route(['/doctor/information/pick'], type='json', auth='public', methods=['POST'])
    def get_doctor_details(self,doctor_id, **post):
        doctor_model = request.env['hr.employee'].sudo().browse(int(doctor_id))
        if doctor_model:

            doctor_details = {
                'doctor_name': doctor_model.name,
                'department_name': doctor_model.department_id.name,

            }
            return {
                'success': True,
                'data': doctor_details,
            }
        else:
            return {
                'success': False,
                'data': {},
            }


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
