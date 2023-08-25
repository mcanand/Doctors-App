from odoo import http
from odoo.http import content_disposition, Controller, request, route
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import datetime, date
import  binascii
import ast
import base64

from base64 import b64encode


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
        doctors = request.env['hr.employee'].sudo().search([('id', 'in', department.member_ids.ids)])
        doctors_list = []  # Change the variable name to doctors_list
        for doctor in doctors:
            det = {
                'name': doctor.name,
                'image_1920': doctor.image_1920,
                'doctor_id' :doctor.id,
            }
            # print(det)
            doctors_list.append(det)

        return http.request.render('web_app_front.department_doctors',
                                   {'doctors': doctors_list, 'department_id': department_id})

    @http.route('/all/doctors', type='http', auth="public", website=True)
    def all_doctors(self, **kw):
        print("ggggggg")
        doctors = request.env['hr.employee'].sudo().search([])  # Retrieve all doctors
        doctor_list = []

        for doctor in doctors:
            values = {
                'name': doctor.name,
                'image_1920': doctor.image_1920,
                'doctor_id':doctor.id,
            }
            doctor_list.append(values)

        return http.request.render('web_app_front.doctors_list', {'doctors_list': doctor_list})

    @http.route(['/fetch/doctor/names'], type='json', auth='public', methods=['POST'])
    def find_doctor_data(self, search_term, **post):
        names = self._fetch_doctor_names(search_term)
        return names

    def _fetch_doctor_names(self, search_term):
        employees = request.env['hr.employee'].sudo().search([
            ('name', 'ilike', search_term),
        ])
        print(employees)
        doctor_data = [{'name': employee.name, 'image_1920': employee.image_1920,'doctor_id':employee.id} for employee in employees]
        return doctor_data
        print(doctor_data)
        return doctor_data

    @http.route(['/fetch/department/doctor/names'], type='json', auth='public', methods=['POST'])
    def find_department_doctor_data(self, search_term, department_id, **post):
        names = self._fetch_department_doctor_names(search_term, department_id)
        return names

    def _fetch_department_doctor_names(self, search_term, department_id):
        employees = request.env['hr.employee'].sudo().search([
            ('name', 'ilike', search_term),
            ('department_id', '=', int(department_id))  # Filter by department_id
        ])

        doctor_data = [{'name': employee.name, 'image_1920': employee.image_1920,'doctor_id':employee.id} for employee in employees]
        return doctor_data

    @http.route('/today/appointment', type='http', auth='public', website=True)
    def view_appointments(self):
        user_partner_id = request.env.user.partner_id
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_ids', 'in', user_partner_id.ids),
            ('booking_button', '=', True),
            ('date', '=', datetime.now().strftime('%Y-%m-%d')),
        ])

        booking_details = []

        for booking in bookings:
            doctor_image_url = booking.doctor_id.image_1920 or ''
            appointment_time = booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'
            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'appointment_time': f"{appointment_time} {am_pm}" ,
                'appointment_end': f"{appointment_end} {ams_pms}" ,
                'doctor_image': doctor_image_url,
                'department': booking.doctor_id.department_id.name,
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
    def get_prescription(self, id, **kw):
        values = {}
        latest_prescription = request.env['doctor.patient.prescription'].sudo().search([
            ('id', '=', id),
        ])
        values['prescription'] = latest_prescription
        print(values)
        return request.render('web_app_front.view_prescription', values)

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
            appointment_time = booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'

            booking_dict = {
                'doctor_name': booking.doctor_id.name,
                'appointment_time':  f"{appointment_time} {am_pm}" ,
                'appointment_end':  f"{appointment_end} {ams_pms}" ,
                'doctor_image': doctor_image_url,
                'id': booking.id,
                'department': booking.doctor_id.department_id.name,
            }

            booking_details.append(booking_dict)
            print(booking_details)

        for previous_booking in previous_bookings:
            doctor_image_url = previous_booking.doctor_id.image_1920 or ''
            appointment_time = previous_booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = previous_booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'
            previous_booking_dict = {
                'doctor_name': previous_booking.doctor_id.name,
                'appointment_time':  f"{appointment_time} {am_pm}" ,
                'appointment_end':  f"{appointment_end} {ams_pms}" ,
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
        print('hhhh')
        return http.request.render('web_app_front.edit_booking_time_template')


    @http.route('/booking/time/update', type='http', auth='public', website=True,)
    def update_booking_time(self, **kw):
        doctor_id = request.env.user.employee_id.id
        print(doctor_id)
        doctor = request.env['hr.employee'].sudo().browse(doctor_id)

        print(doctor)
        date = kw.get('date')
        from_time = kw.get('from_time')
        to_time = kw.get('to_time')
        from_time_str = from_time.replace(':', '.')
        to_time_str = to_time.replace(':', '.')
        slot = request.env['doctor.time.slots'].sudo().search([('date', '=', date)])
        if slot:
           doctor.write({
            'date': date,
            'time_from': from_time_str,
            'time_to': to_time_str,
           })
        else:
            return "please enter a valid date to change the slot time."
        return request.redirect('/my')

    @http.route('/today/appointment/doctor', type='http', auth='public', website=True)
    def view_appointments_doctor(self):
        doctor_id = request.env.user.employee_id
        bookings = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', doctor_id.id),
            ('booking_button', '=', True),
            ('date', '=', datetime.now().strftime('%Y-%m-%d')),
            ('prescription_status', '=', False)
        ])

        booking_details = []
        group_patient_bookings = []

        for booking in bookings:
            patient_names = [partner.name for partner in booking.partner_ids]
            patient_name = ', '.join(patient_names)
            partner_ids = [partner.id for partner in booking.partner_ids]
            appointment_time = booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'
            booking_dict = {
                'patient_name': patient_name,
                'group_meeting':booking.group_meeting,
                'patient_id': partner_ids,
                'appointment_time': f"{appointment_time} {am_pm}" ,
                'appointment_end': f"{appointment_end} {ams_pms}",
                'id': booking.id,
            }
            if len(partner_ids) > 1:
                group_patient_bookings.append(booking_dict)
            else:
                booking_details.append(booking_dict)

        return request.render('web_app_front.today_appointment_doctor', {'appointments': booking_details,'group_patient_appointments': group_patient_bookings})


    @route('/all/appointment/doctor', type='http', auth='public', website=True)
    def all_appointments_doctor(self, **kwargs):
        doctor_id = request.env.user.employee_id
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
        doctor_name=doctor_id.name
        booking_details = []
        previous_booking_details = []

        for booking in bookings:
            patient_names = [partner.name for partner in booking.partner_ids]
            patient_name = ', '.join(patient_names)
            partner_ids = [partner.id for partner in booking.partner_ids]
            appointment_time = booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'

            booking_dict = {

                'patient_name': patient_name,
                'group_meeting':booking.group_meeting,
                'appointment_time': f"{appointment_time} {am_pm}",
                'appointment_end':  f"{appointment_end} {ams_pms}",
                'id': booking.id,
                'date': booking.date,
                'patient_id': partner_ids,

            }

            booking_details.append(booking_dict)
            print(booking_details)
        for previous_booking in previous_bookings:
            patient_names = [partner.name for partner in previous_booking.partner_ids]
            patient_name = ', '.join(patient_names)
            partner_ids = [partner.id for partner in previous_booking.partner_ids]
            appointment_time = previous_booking.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = previous_booking.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'
            previous_booking_dict = {
                'patient_name': patient_name,
                'appointment_time': f"{appointment_time} {am_pm}",
                'appointment_end': f"{appointment_end} {ams_pms}",
                'date': previous_booking.date,
                'patient_id': partner_ids,

            }

            previous_booking_details.append(previous_booking_dict)
            print(previous_booking_details)
        return http.request.render('web_app_front.all_appointment_doctor', {
            'appointments': booking_details,
            'previous_appointments': previous_booking_details,'doctor_name':doctor_name,
        })

    @http.route(['/doctor/information/pick'], type='json', auth='public', methods=['POST'])
    def get_doctor_details(self, doctor_id, **post):
        print(doctor_id)
        doctor_model = request.env['hr.employee'].sudo().browse(int(doctor_id))
        if doctor_model:
            doctor_details = {
                'doctor_name': doctor_model.name,
                'department_name': doctor_model.department_id.name,
                'image': doctor_model.image_1920,
                'experience': doctor_model.work_experience,
                'about': doctor_model.about,
                'doctor_id': doctor_model.id,

            }
            rating_model = request.env['doctor.rating']
            rating_record = rating_model.sudo().search([('doctor_id', '=', doctor_model.id)], limit=1)
            if rating_record:
                doctor_details['rating'] = rating_record.rating

            return {
                'data': doctor_details,
            }
        else:
            return {
                'error': ('Doctor not found.'),
            }



    @http.route(['/booking/availability/<int:id>'], type='http', auth='public', website=True)
    def booking_availability(self, id, **kw):
        today = date.today()
        available_slots = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', id),
            ('booking_button', '!=', True),
            ('date', '>', today.strftime('%Y-%m-%d'))
        ])

        booking_details = []
        one_hour_fee= available_slots.doctor_id.one_hour_fee
        doctor=available_slots.doctor_id.name
        department = available_slots.doctor_id.department_id.name

        for slot in available_slots:
            doctor_details = {
                'doctor_name': slot.doctor_id.name,
                'date': slot.date,
                'from_time': slot.from_time,
                'to_time': slot.to_time,
                'slot_id': slot.id,

            }
            booking_details.append(doctor_details)

        return http.request.render('web_app_front.booking_availability', {'available_slots': booking_details,'department':department,'doctor':doctor,'one_hour_fee':one_hour_fee})



    @http.route(['/prescription/add/<string:id>'], type='http', auth='user', website=True)
    def add_prescription(self,id, **kw):
        print(id)
        val = ast.literal_eval(id)
        partner_count = len(val)
        if partner_count == 1 :
         patient_details = request.env['res.partner'].sudo().browse(val)
        else:
            patient_details =None
        current_date=date.today()
        return http.request.render('web_app_front.add_prescription',{'patient_details' :patient_details,'partner_count': partner_count,'patient_id':id,'current_date' :current_date})

    # @http.route('/prescription/save', type='http', auth='user', website=True, csrf=True)
    # def save_prescription(self, **kw):
    #     # Extract data from request parameters
    #     patient_ids_str = kw.get('patient_id')
    #     patient_ids_list = [int(id) for id in patient_ids_str.strip('[]').split(',') if id.strip().isdigit()]
    #     doctor_id = request.env.user.employee_ids.ids[0]
    #     case_details = kw.get('case')
    #     prescription = kw.get('pres')
    #     next_sitting = kw.get('next_sitting')
    #     from_time = kw.get('froms')
    #     to_time = kw.get('to')
    #     next_sitting_date = kw.get('next_sitting_date')
    #     from_time_det = kw.get('from_time')
    #     to_time_det = kw.get('to_time')
    #     froms = format(from_time).replace('.', ':')
    #     to = format(to_time).replace('.', ':')
    #     from_time = format(from_time_det).replace('.', ':')
    #     to_time = format(to_time_det).replace('.', ':')
    #     print(from_time)
    #
    #
    #     # Get model instances
    #     prescription_det = request.env['doctor.patient.prescription'].sudo()
    #     time_slots = request.env['doctor.time.slots'].sudo()
    #
    #     # Loop through patient IDs
    #     for patient_id in patient_ids_list:
    #         # Create prescription entry
    #         prescription_det.create({
    #             'partner_ids': [(4, patient_id)],
    #             'case_details': case_details,
    #             'prescription': prescription,
    #             'doctor_id': doctor_id,
    #             'date': date.today(),
    #             'prescription_status': True,
    #         })
    #     if next_sitting:
    #             # Update existing slot or create new slot
    #         existing_slot = time_slots.search([
    #                 ('doctor_id', '=', doctor_id),
    #                 ('date', '=', next_sitting),
    #                 ('from_time', '=', froms),
    #                 ('to_time', '=', to),
    #         ], limit=1)
    #         print(existing_slot.booking_button)
    #         if existing_slot:
    #                 if existing_slot.booking_button:
    #                     return "This time slot is already booked. Please choose another time."
    #                 else:
    #                     existing_slot.write({
    #                         'booking_button': True,
    #                         'partner_ids':  [(4, partner_id) for partner_id in patient_ids_list],
    #                     })
    #         else:
    #                 new_slot = time_slots.create({
    #                     'partner_ids':  [(4, partner_id) for partner_id in patient_ids_list],
    #                     'doctor_id': doctor_id,
    #                     'date': next_sitting,
    #                     'from_time': froms,
    #                     'to_time': to,
    #                     'booking_button': True,
    #                 })
    #     if next_sitting_date:
    #                 # Update existing slot or create new slot
    #             existing_slot_detail = time_slots.search([
    #                     ('doctor_id', '=', doctor_id),
    #                     ('date', '=', next_sitting_date),
    #                     ('from_time', '=', from_time),
    #                     ('to_time', '=', to_time),
    #             ])
    #             print(existing_slot_detail.booking_button)
    #             if existing_slot_detail:
    #                     if existing_slot_detail.booking_button:
    #                         return "This time slot is already booked. Please choose another time."
    #                     else:
    #                         existing_slot_detail.write({
    #                             'booking_button': True,
    #                             'partner_ids':  [(4, partner_id) for partner_id in patient_ids_list],
    #                         })
    #             else:
    #                     new_slots = time_slots.create({
    #                         'partner_ids':  [(4, partner_id) for partner_id in patient_ids_list],
    #                         'doctor_id': doctor_id,
    #                         'date': next_sitting_date,
    #                         'from_time': from_time,
    #                         'to_time': to_time,
    #                         'booking_button': True,
    #                     })
    #
    #     return request.redirect('/today/appointment/doctor')
    #
    #

    @http.route('/prescription/save', type='http', auth='user', website=True, csrf=True)
    def save_prescription(self, **kw):
        # Extract data from request parameters
        patient_ids_str = kw.get('patient_id')
        patient_ids_list = [int(id) for id in patient_ids_str.strip('[]').split(',') if id.strip().isdigit()]
        doctor_id = request.env.user.employee_id.id
        case_details = kw.get('case')
        prescription = kw.get('pres')
        next_sitting = kw.get('next_sitting')
        from_time = kw.get('froms')
        to_time = kw.get('to')
        next_sitting_date = kw.get('next_sitting_date')
        from_time_det = kw.get('from_time')
        to_time_det = kw.get('to_time')
        froms = format(from_time).replace('.', ':')
        to = format(to_time).replace('.', ':')
        from_time = format(from_time_det).replace('.', ':')
        to_time = format(to_time_det).replace('.', ':')

        # Get model instances
        prescription_det = request.env['doctor.patient.prescription'].sudo()
        time_slots = request.env['doctor.time.slots'].sudo()

        # Loop through patient IDs
        for patient_id in patient_ids_list:
            # Create prescription entry
            prescription_det.create({
                'partner_ids': [(4, patient_id)],
                'case_details': case_details,
                'prescription': prescription,
                'doctor_id': doctor_id,
                'date': datetime.today().date(),
                'prescription_status': True,
            })
            related_slots = time_slots.search([('partner_ids', 'in', [patient_id])])
            related_slots.write({'prescription_status': True})

        # Check and create/update slots for next sitting
        if next_sitting:
            result = self._create_or_update_slot(time_slots, doctor_id, next_sitting, froms, to, patient_ids_list)
            if isinstance(result, str):
                return result

        # Check and create/update slots for next sitting date
        if next_sitting_date:
            result = self._create_or_update_slot(time_slots, doctor_id, next_sitting_date, from_time, to_time,
                                                 patient_ids_list)
            if isinstance(result, str):
                return result

        return request.redirect('/today/appointment/doctor')

    def _create_or_update_slot(self, time_slots, doctor_id, date, from_time, to_time, patient_ids_list):
        overlapping_slots = time_slots.search([
            ('doctor_id', '=', doctor_id),
            ('date', '=', date),
            '|', '|',
            ('from_time', '<', from_time),
            ('to_time', '>', from_time),
            ('from_time', '<', to_time),
            ('to_time', '>', to_time),
        ])

        if overlapping_slots:
            return "There is an booking. Please choose another time."

        existing_slot = time_slots.search([
            ('doctor_id', '=', doctor_id),
            ('date', '=', date),
            ('from_time', '=', from_time),
            ('to_time', '=', to_time),
        ], limit=1)

        if existing_slot:
            if existing_slot.booking_button:
                return "This time slot is already booked. Please choose another time."
            else:
                existing_slot.write({
                    'booking_button': True,
                    'partner_ids': [(4, partner_id) for partner_id in patient_ids_list],
                })
        else:
            new_slot = time_slots.create({
                'partner_ids': [(4, partner_id) for partner_id in patient_ids_list],
                'doctor_id': doctor_id,
                'date': date,
                'from_time': from_time,
                'to_time': to_time,
                'booking_button': True,
            })

        return None




    @http.route(['/book/now'], type='json', auth='public', website=True, methods=['POST'])
    def book_now(self, slot_id, **kw):
        Slot = request.env['doctor.time.slots'].sudo()
        slot = Slot.browse(int(slot_id))
        print(slot)
        if not slot.partner_ids:
            patient_id = request.env.user.partner_id.id
            print(patient_id)
            slot.write({
                'partner_ids': [(4, patient_id, 0)],
            })
            slot.on_partner_id_change()

        return True

    @http.route(['/enter/details'], type='http', auth='public', website=True)
    def enter_details(self, **kw):
        departments = request.env['hr.department'].sudo().search([])
        countries = http.request.env['res.country'].sudo().search(
            [('code', '=', 'IN')])  # Get country with code 'IN' for India
        india_states = http.request.env['res.country.state'].sudo().search([('country_id', 'in', countries.ids)])
        return http.request.render('web_app_front.enter_details',{'departments': departments, 'states': india_states})

    @http.route('/doctor/details/save', type='http', auth='user', website=True)
    def add_doctor(self, **kw):
        # file = kw.get('image_1920').filename()
        # print(file)

        request.env['doctor.details'].sudo().create({
            'department_id': kw.get('department_id'),
            'name': kw.get('name'),
            'gender': kw.get('gender'),
            'mobile': kw.get('mobile'),
            'email': kw.get('email'),
            'experience': kw.get('experience'),

            'state_id': kw.get('state_id'),
            # 'profile_pic':base64.b64encode(file),
            'time_from': kw.get('time_from'),
            'time_to': kw.get('time_to'),
            'work_address': kw.get('work_address'),
            'about': kw.get('about'),
            'private_contact_address': kw.get('address'),
            'emergency_contact_phone': kw.get('contact'),

        })

        return request.redirect('/web/login')

    @http.route('/group/sessions', type='http', auth='public', website=True)
    def group_details(self, **kw):
        today = datetime.now().date()

        # Retrieve doctor.time.slots records with non-empty group_meeting from today onwards
        slots = http.request.env['doctor.time.slots'].sudo().search([
            ('group_meeting', '!=', False),
            ('date', '>=', today),
        ])
        booking_details=[]
        for slot in slots:
            appointment_time = slot.from_time
            appointment_hour = int(appointment_time.split(':')[0])
            am_pm = 'AM' if 0 <= appointment_hour < 12 else 'PM'
            appointment_end = slot.to_time
            appointment_hours = int(appointment_end.split(':')[0])
            ams_pms = 'AM' if 0 <= appointment_hours < 12 else 'PM'
            doctor_details = {
                'doctor_name': slot.doctor_id.name,
                'department_name': slot.doctor_id.department_id.name,
                'date': slot.date,
                'doctor_image':slot.doctor_id.image_1920,
                'from_time': f"{appointment_time} {am_pm}",
                'to_time': f"{appointment_end} {ams_pms}",
                'slot_id': slot.id,

            }
            booking_details.append(doctor_details)
        return http.request.render('web_app_front.group_details', {'appointments' : booking_details})



    @http.route(['/join/group/meetings/<int:slot_id>'], type='http', auth='public', website=True)
    def join_group_meeting(self, slot_id, **kw):
        group_slot = request.env['doctor.time.slots'].sudo().browse(slot_id)
        partner_id = request.env.user.partner_id.id
        group_slot.write({'partner_ids': [(4, partner_id)]})
        print('kkkk')

        return request.redirect('/group/sessions')


    @http.route('/create/meeting', type='http', auth='public', website=True)
    def create_meeting_date(self, **kw):
        return http.request.render('web_app_front.create_meeting')


    @http.route('/create/new/meeting', type='http', auth='public', website=True)
    def create_booking_time(self, **kw):
        employee =request.env.user.employee_id
        date = kw.get('date')
        from_time = kw.get('from_time')
        to_time = kw.get('to_time')
        name = kw.get('name')
        existing_slot = request.env['doctor.time.slots'].search([
            ('doctor_id', '=', employee.id),
            ('date', '=', date),
            ('from_time', '=', from_time),
            ('to_time', '=', to_time),
        ], limit=1)

        if existing_slot:
            if not existing_slot.partner_ids:
                # Slot exists but has no partners, update the slot name
                existing_slot.write({
                    'group_meeting': name,
                })
                return None

            if existing_slot.booking_button:
                return "This time slot is already booked. Please choose another time."

            # Check for overlapping slots
        overlapping_slots = request.env['doctor.time.slots'].search([
                ('doctor_id', '=', employee.id),
                ('date', '=', date),
                '|', '|',
                ('from_time', '<', from_time),
                ('to_time', '>', from_time),
                ('from_time', '<', to_time),
                ('to_time', '>', to_time),
            ])

        if overlapping_slots:
                return "There is a booking. Please choose another time."


        else:
            #Create a new slot
            new_slot = request.env['doctor.time.slots'].create({

                'doctor_id': employee.id,
                'date': date,
                'from_time': from_time,
                'to_time': to_time,
                'group_meeting': name,

            })

        return request.redirect('/my')


    @http.route('/add/extra/slot', type='http', auth='public', website=True)
    def create_meeting(self, **kw):
        return http.request.render('web_app_front.add_extra_slot')

    @http.route('/create/extra/slot', type='http', auth='public', website=True)
    def create_extra_time(self, **kw):
        employee = request.env.user.employee_id
        date = kw.get('date')
        from_time = kw.get('from_time')
        to_time = kw.get('to_time')
        existing_slot = request.env['doctor.time.slots'].search([
            ('doctor_id', '=', employee.id),
            ('date', '=', date),
            ('from_time', '=', from_time),
            ('to_time', '=', to_time),
        ], limit=1)

        if existing_slot:
                return "This time slot is already created. Please choose another time."

        overlapping_slots = request.env['doctor.time.slots'].search([
            ('doctor_id', '=', employee.id),
            ('date', '=', date),
            '|', '|',
            ('from_time', '<', from_time),
            ('to_time', '>', from_time),
            ('from_time', '<', to_time),
            ('to_time', '>', to_time),
        ])

        if overlapping_slots:
            return "There is a slot. Please choose another time."


        else:
            # Create a new slot
            new_slot = request.env['doctor.time.slots'].create({

                'doctor_id': employee.id,
                'date': date,
                'from_time': from_time,
                'to_time': to_time,

            })

        return request.redirect('/my')







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
