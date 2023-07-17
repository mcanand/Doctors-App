from odoo import http
from odoo.http import request
import base64
from datetime import datetime


class SignupPageController(http.Controller):
    @http.route('/signup-page', type='http', auth='public')
    def signup_page(self):
        return request.render('doctor_website.signup_page_template')

    @http.route('/doctor/enter/details', type='http', auth='public')
    def enter_details_page(self):
        departments = request.env['hr.department'].sudo().search([])
        countries = http.request.env['res.country'].sudo().search(
            [('code', '=', 'IN')])  # Get country with code 'IN' for India
        india_states = http.request.env['res.country.state'].sudo().search([('country_id', 'in', countries.ids)])
        return request.render('doctor_website.doctor_enter_details',
                              {'departments': departments, 'states': india_states})

    @http.route('/doctor/details/save', type='http', auth='user', website=True)
    def add_doctor(self, *args, **kw):
        profile_pic = kw.get('image')
        if profile_pic:
            profile_pic_bytes = profile_pic.encode('utf-8')
            profile_pic_base64 = base64.b64encode(profile_pic_bytes).decode('utf-8')


        doctor_vals = {
            'department_id': kw.get('department_id'),
            'name': kw.get('name'),
            'gender': kw.get('gender'),
            'mobile': kw.get('mobile'),
            'email': kw.get('email'),
            'experience': kw.get('experience'),
            # 'profile_pic': profile_pic_base64,
            'state_id': kw.get('state_id'),
            'time_from':kw.get('time_from'),
            'time_to' :kw.get('time_to'),
            'work_address': kw.get('work_address'),
            'about': kw.get('about'),
            'private_contact_address': kw.get('address'),
            'emergency_contact_phone': kw.get('contact'),
            # Set other fields accordingly
        }
        doctor = request.env['doctor.details'].sudo().create(doctor_vals)
        # Save the profile picture
        # profile_pic = kw.get('image')
        # if profile_pic:
        #     profile_pic_bytes = profile_pic.encode('utf-8')
        #     profile_pic_base64 = base64.b64encode(profile_pic_bytes).decode('utf-8')
            # attachment = request.env['ir.attachment'].sudo().create({
            #     'name': 'Profile Picture',
            #     'datas': profile_pic_base64,
            #     'res_model': 'doctor.details',
            #     'res_id': doctor.id,
            #     'mimetype': 'image/jpeg',
            # })
            # doctor.profile_pic = attachment.datas

        return request.redirect('/web/login')


    # @http.route()
    # def edit_employee_details(self, **post):
    #     user = request.env.user
    #     if user.partner_id and user.partner_id.cate_id == 'doctor':
    #         return request.redirect('/doctor/my')
    #     elif user.partner_id and user.partner_id.cate_id == 'patient':
    #         return request.redirect('/patient/my')
    #     else:
    #         return request.redirect('/my')

