from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from datetime import datetime,date
import base64



class MyDashboard(CustomerPortal):

    #departments of doctors
    @http.route(['/department/list'], type='http', auth='user', website=True,
                methods=['GET', 'POST'])
    def my_dashboard(self, search=None, **post):
        domain = []
        if search:
            domain += [('name', 'ilike', search)]

        departments = request.env['hr.department'].sudo().search(domain)

        online_doctors = request.env['hr.employee'].sudo().search([])
        # all_doctors = request.env['hr.employee'].sudo().search([])

        return request.render("doctor_website.portal_my_dashboard", {
            'departments': departments,
            'search': search,
            'online_doctors': online_doctors,
            # 'all_doctors': all_doctors,
        })


   #find all doctors
    @http.route(['/all/doctor'], type='http', auth="user", website=True)
    def display_doctor(self, **kwargs):
        doctor = request.env['hr.employee'].sudo().search([])

        values = {
            'doctor': doctor,
        }
        print(values)
        return http.request.render('doctor_website.view_alldoctor_detail_mobile', values)



    #find  doctor details
    @http.route(['/doctor/details/<int:doctor_id>'], type='http', auth="user", website=True)
    def display_doctor_details(self, doctor_id, **kwargs):
        doctor = request.env['hr.employee'].sudo().browse(doctor_id)

        values = {
            'doctor': doctor,
        }
        return http.request.render('doctor_website.view_doctor_detail_mobile', values)

   #find department vice doctors
    @http.route(['/department/doctor/<int:department_id>'], type='http', auth="user", website=True)
    def display_doctors(self, department_id, **kwargs):
        department = request.env['hr.department'].sudo().browse(department_id)
        doctors = department.member_ids
        values = {
            'doctors': doctors,
        }
        return http.request.render('doctor_website.view_department_doctor_list', values)

    #find available slots with particular doctor search
    @http.route(['/doctor/available/slots/<int:doctor_id>'], type='http', auth="user", website=True)
    def display_available_slots(self, doctor_id, **kwargs):
        today = datetime.now().date()
        doctor = request.env['hr.employee'].sudo().browse(doctor_id)
        slots = request.env['doctor.time.slots'].search([
            ('doctor_id', '=', doctor.id),
            ('date', '>=', today),
            ('partner_id', '=', False),  # Filter slots with no partner ID
        ])

        values = {
            'doctor': doctor,
            'slots': slots,
        }
        return http.request.render('doctor_website.view_doctor_available_slots_mobile', values)

    #booking a slot
    @http.route(['/doctor/book/slot/<int:slot_id>'], type='http', auth="user", website=True)
    def book_slot(self, slot_id, **kwargs):
        Slot = request.env['doctor.time.slots'].sudo()
        slot = Slot.browse(slot_id)
        print(slot)
        if not slot.partner_id:
            # Set the partner ID to the current user's partner
            slot.partner_id = request.env.user.partner_id.id
            # Call the onchange function
            slot.on_partner_id_change()
            # Redirect to the success page
            return  http.request.render('doctor_website.view_success_page_mobile')
        else:
            # Redirect to the error page
            return  http.request.render('doctor_website.view_error_page_mobile')


    #view doctor available slots
    @http.route('/doctor/get/slots', type='json', auth='public', website=True)
    def get_active_slots(self, category_id):
      user = request.env.user
      if category_id == 'user':
        today = date.today()
        slots = request.env['doctor.time.slots'].sudo().search(
                    [('partner_id', '=', user.partner_id.id), ('date', '>=', today), ('booking_button', '=', True)])

      return {'slots': slots}

    #view patient prescription list
    @http.route('/added/prescription/list', type='http', auth='user', website=True)
    def added_prescription_list(self, **kw):
        user = request.env.user.partner_id
        print(user)
        prescriptions = request.env['doctor.patient.prescription'].sudo().search([('partner_id', '=', user.id)])
        print(prescriptions)
        return http.request.render('doctor_website.added_prescription_list', {
            'prescriptions': prescriptions
        })

#   view patient prescription
    @http.route('/view/prescription/<int:prescription_id>', type='http', auth='user', website=True)
    def view_prescription(self, prescription_id, **kwargs):
        prescription = request.env['doctor.patient.prescription'].sudo().browse(prescription_id)
        return http.request.render('doctor_website.view_prescription', {'prescription': prescription})


    #booked appoinments
    @http.route('/appointments', type='http', auth='user', website=True)
    def view_appoinments(self, **kwargs):
      bookings = request.env['doctor.time.slots'].sudo().search([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('booking_button', '=', True)
        ])
      booking_details = []

      for booking in bookings:
          booking_dict = {
              'doctor_name': booking.doctor_id.name,
              'appoinment_time': booking.display_time_interval,
              'date': booking.date,
              'meeting_link':booking.meeting_link,
          }

          booking_details.append(booking_dict)
          print(booking_details)
      return http.request.render('doctor_website.appoinments', {'appointments': booking_details})



    #save lab attachment

    @http.route('/lab/attachment/save', type='http', auth='user', website=True)
    def lab_prescription(self, **kw):
        prescription_id = kw.get('prescription_id')
        lab_attachment = kw.get('lab_attachment')
        lab_attachment_data = False

        if lab_attachment:
            lab_attachment_data = base64.b64encode(lab_attachment.encode('UTF-8'))

        prescription = request.env['doctor.patient.prescription'].sudo().browse(prescription_id)
        attachment_data = {
            'mimetype': lab_attachment,
            'attachment': lab_attachment_data or False,
        }
        attachment = request.env['lab.attachment'].sudo().create(attachment_data)

        if attachment:
            prescription.lab_attachment = [(4, attachment.id, 0)]

        return request.redirect('/added/prescription/list')

