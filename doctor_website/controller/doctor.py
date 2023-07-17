from odoo import http
from odoo.http import request,werkzeug
from datetime import date,datetime
from werkzeug.utils import redirect


class EmployeeController(http.Controller):


    #edit doctor details page
    @http.route('/doctor/edit', type='http', auth='user', website=True)
    def edit_employee_details(self, **post):
        doctor_id = request.env.user.employee_ids and request.env.user.employee_ids[0].id
        print(doctor_id)
        doctor = request.env['hr.employee'].sudo().browse(doctor_id)
        if doctor:

            print(doctor.address_id.name)  # Check the value of address_id
            print(doctor.work_location_id.name)
            print(doctor.about)  # Check the value of address_id
            print(doctor.date)
            departments = request.env['hr.department'].sudo().search([])
            return request.render('doctor_website.edit_doctor_details', {'doctor': doctor, 'departments': departments})

    #save edited details
    @http.route('/doctor/save', type='http', auth='user', website=True)
    def edit_employee(self, *args, **kw):
        doctor_id = request.env.user.employee_ids and request.env.user.employee_ids[0].id
        if doctor_id:
            doctor = request.env['hr.employee'].sudo().browse(doctor_id)
            department_id = int(kw.get('department_id'))
            # address_id = kw.get('address_id')
            # work_location_id = kw.get('work_location_id')
            work_experience = kw.get('work_experience')
            date = kw.get('date')
            time_from = kw.get('time_from')
            time_to = kw.get('time_to')
            about = kw.get('about')
            print(department_id)
            doctor.write({
                'department_id': department_id,
                # 'address_id': address_id,
                # 'work_location_id': work_location_id,
                'work_experience': work_experience,
                'date': date,
                'time_from': time_from,
                'time_to': time_to,
                'about': about,
            })
            return request.redirect('/my')

    #today's booking details of doctor
    @http.route('/today/booking', type='http', auth='user', website=True)
    def todays_booking(self, **kwargs):
        today = date.today()
        booking_model = request.env['doctor.time.slots']
        # doctor_id = request.env.user.employee_id.id
        doctor_id = request.env.user.employee_ids and request.env.user.employee_ids[0].id
        bookings = booking_model.search(
            [('date', '=', today), ('doctor_id', '=', doctor_id), ('booking_button', '=', True)])

        booking_details = []

        for booking in bookings:
            partner = request.env['res.partner'].sudo().browse(booking.partner_id.id)
            patient_name = partner.name if partner else ''
            print(patient_name)
            booking_dict = {
                'patient_name': patient_name,
                'patient_id': booking.partner_id,
                'appoinment_time': booking.display_time_interval,
            }

            booking_details.append(booking_dict)

        return http.request.render('doctor_website.todays_booking_details', {'bookings': booking_details})



    # all booking details of doctor
    @http.route('/all/booking', type='http', auth='user', website=True)
    def all_booking(self, **kwargs):
        today = date.today()
        booking_model = request.env['doctor.time.slots']
        doctor_id = request.env.user.employee_ids and request.env.user.employee_ids[0].id
        bookings = booking_model.search(
            [('date', '>=', today), ('doctor_id', '=', doctor_id), ('booking_button', '=', True)])

        booking_details = []

        for booking in bookings:
            partner = request.env['res.partner'].sudo().browse(booking.partner_id.id)
            patient_name = partner.name if partner else ''
            print(patient_name)
            booking_dict = {
                'patient_name': patient_name,
                'appoinment_time': booking.display_time_interval,
                'date': booking.date,
            }

            booking_details.append(booking_dict)

        return http.request.render('doctor_website.all_booking_details', {'bookings': booking_details,})


    #to display prescription page
    @http.route(['/today/add/prescription/<int:patient_id>'], type='http', auth='user', website=True)
    def add_prescription(self,patient_id, **kwargs):
        patient= request.env['res.partner'].sudo().browse(patient_id)
        prescription = request.env['doctor.patient.prescription'].sudo().browse(patient_id)
        previous_histories = request.env['doctor.patient.prescription'].sudo().search([
            ('partner_id', '=', patient_id)
        ], limit=5, order='date desc')

        return http.request.render('doctor_website.doctor_enter_prescription',{'patient' :patient,  'previous_histories': previous_histories,
        'selected_history': False})



    @http.route('/get/history', type='json', auth='user', website=True)
    def get_history(self, **kw):
        history_id = int(kw.get('history_id'))
        history = request.env['doctor.patient.prescription'].sudo().browse(history_id)

        return request.render('doctor_website.doctor_history_details', {'selected_history': history})

    #save prescription
    @http.route('/prescription/save', type='http', auth='user', website=True, csrf=True)
    def save_prescription(self, **kw):
        doctor_id = request.env.user.employee_ids.ids[0]  # Get the ID of the doctor from the employee_ids
        patient_id = int(kw.get('patient_id'))
        case_details = kw.get('case')
        # lab_details = kw.get('lab')
        prescription = kw.get('prescription')
        print(doctor_id)
        print(case_details)
        print(prescription)
        print(patient_id)
        prescription_det = request.env['doctor.patient.prescription'].sudo()
        prescription_det.create({
            'partner_id': patient_id,
            'case_details': case_details,
            # 'lab_attachment': lab_details,
            'prescription': prescription,
            'doctor_id': doctor_id
        })

        return request.redirect('/today/booking')


    #view all prescriptions
    @http.route(['/today/edit/prescription/<int:patient_id>'], type='http', auth='user', website=True)
    def edit_prescription(self, patient_id, **kwargs):
        print(patient_id)
        prescriptions = request.env['doctor.patient.prescription'].sudo().search([('partner_id', '=', patient_id)])

        print(prescriptions)
        prescription_details = []
        for prescription in prescriptions:
            try:
                booking_dict = {
                    'doctor_name': prescription.doctor_id.name,
                    'date': prescription.date,
                    'prescription_id': prescription.id,
                }
                prescription_details.append(booking_dict)
                print(prescription_details)
            except Exception as e:
                print(f"An error occurred: {e}")
        return http.request.render('doctor_website.view_prescription_details',
                                   {'patient_id': patient_id, 'prescriptions': prescription_details})

    #view selected prescription
    @http.route(['/today/edit/prescription/view/prescription/<int:prescription_id>'], type='http', auth='user', website=True)
    def view_prescription(self, prescription_id, **kwargs):
        prescription = request.env['doctor.patient.prescription'].sudo().browse(prescription_id)
        return http.request.render('doctor_website.view_prescription_doctor', {'prescription': prescription})



    #next available dates of doctor ,for checking booking availabilty
    @http.route(['/available/booking/slot/<int:patient_id>'], type='http', auth='user', website=True)
    def next_available_dates(self, patient_id, **kwargs):
        doctor = request.env.user.employee_ids
        current_date = datetime.now().date()

        slots = request.env['doctor.time.slots'].sudo().search([
            ('doctor_id', '=', doctor.id),
            ('booking_button', '=', False),
            ('date', '>', current_date)
        ],order = 'date, display_time_interval')
        return http.request.render('doctor_website.patient_next_booking',{'slots':slots,'patient_id':patient_id})

    # doctor booking next visit date to the partner
    @http.route('/doctor/book/slot/<int:slot_id>/<int:patient_id>', type='http', auth='user', website=True)
    def book_slot(self, slot_id, patient_id, **kwargs):
        slot = request.env['doctor.time.slots'].sudo().browse(slot_id)
        patient = request.env['res.partner'].sudo().browse(patient_id)
        if not slot.partner_id:
            # Set the partner ID to the patient's ID
            slot.partner_id = patient.id
            slot.on_partner_id_change()
            # Redirect to the success page
            return http.request.render('doctor_website.view_success_page_mobile')
        else:
            # Redirect to the error page
            return http.request.render('doctor_website.view_error_page_mobile')