from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date,datetime, timedelta
import requests
import json

class Doctor(models.Model):
    _inherit = 'hr.employee'

    date = fields.Date(default=lambda self: datetime.now().date() + timedelta(days=1))
    time_from = fields.Float(string='From')
    time_to = fields.Float(string='To')
    partner_ids = fields.Many2many('res.partner', string='Partner')
    slots_ids = fields.One2many('doctor.time.slots', 'doctor_id')
    prescription_ids = fields.One2many('doctor.patient.prescription', 'doctor_id', string='Prescriptions')
    doctor_category_ids = fields.Many2many('hr.employee.category', string='Doctor Categories')
    work_experience = fields.Integer(string='Work Experience (in years)')
    stars_earned = fields.Integer(string='Stars Earned')
    about = fields.Text(string='About')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender'
    )
    work_address = fields.Text(string='Work Address')
    CATEGORY_SELECTION = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    cate_id = fields.Selection(CATEGORY_SELECTION, string='Category', required=True)
    one_hour_fee = fields.Float(string='Sitting fee per hour', digits=(10, 2), default=0.0)



    @api.model_create_multi
    def create(self, vals_list):
        res = super(Doctor, self).create(vals_list)
        for record_vals, record in zip(vals_list, res):
            if record_vals.get('time_from') and record_vals.get('time_to'):
                if record_vals['time_from'] > record_vals['time_to']:
                    raise ValidationError().new("Invalid time interval: time_from should be less than time_to")

            intervals = record._get_time_intervals(record_vals.get('time_from'), record_vals.get('time_to'))
            current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
            end_date = current_date + timedelta(days=15)

            while current_date <= end_date:
                slots = self.env['doctor.time.slots']
                for from_time, to_time in intervals:
                    display_interval = f'From {from_time} to {to_time}'
                    slots |= self.env['doctor.time.slots'].create({
                        'doctor_id': record.id,
                        'partner_ids': [(6, 0, record.partner_ids.ids)],
                        'date': current_date.strftime("%Y-%m-%d"),
                        'from_time': from_time,
                        'to_time': to_time,
                        'display_time_interval': display_interval,
                    })
                current_date += timedelta(days=1)
        return res

    def _get_time_intervals(self, time_from, time_to):
        intervals = []
        interval = time_from
        while interval < time_to:
            hour_start = int(interval)
            minute_start = int((interval - hour_start) * 60)

            interval += 0.5
            hour_end = int(interval)
            minute_end = int((interval - hour_end) * 60)

            time_str_start = "{:02d}:{:02d}".format(hour_start, minute_start)
            time_str_end = "{:02d}:{:02d}".format(hour_end, minute_end)

            intervals.append((time_str_start, time_str_end))
        return intervals


    def write(self, vals):
        res = super(Doctor, self).write(vals)

        if any(field_name in vals for field_name in ('time_from', 'time_to', 'date')):
            for doctor in self:
                if doctor.time_from and doctor.time_to and doctor.date:
                    if doctor.time_from > doctor.time_to:
                        raise ValidationError("Invalid time interval: time_from should be less than time_to")

                    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                    end_date = start_date + timedelta(days=15)

                    slots = self.env['doctor.time.slots'].search([
                        ('doctor_id', '=', doctor.id),
                        ('date', '>=', start_date.strftime("%Y-%m-%d")),
                        ('date', '<=', end_date.strftime("%Y-%m-%d"))
                    ])

                    # Remove existing slots
                    slots.unlink()

                    # Generate new slots
                    current_date = start_date
                    while current_date <= end_date:
                        intervals = doctor._get_time_intervals(doctor.time_from, doctor.time_to)
                        for from_time, to_time in intervals:
                            display_interval = f'From {from_time} to {to_time}'
                            self.env['doctor.time.slots'].create({
                                'doctor_id': doctor.id,
                                'partner_ids': [(6, 0, doctor.partner_ids.ids)],
                                # 'partner_ids': doctor.partner_ids.id,
                                'date': current_date.strftime("%Y-%m-%d"),
                                'from_time': from_time,
                                'to_time': to_time,
                                'display_time_interval': display_interval,
                            })
                        current_date += timedelta(days=1)

        if 'display_time_interval' in vals:
            for doctor in self:
                # Extract 'from_time' and 'to_time' from the 'display_time_interval' when it's being updated
                from_time_str, to_time_str = vals.get('display_time_interval', '').split(' to ')
                doctor.time_from = float(from_time_str.split(':')[0]) + float(from_time_str.split(':')[1]) / 60
                doctor.time_to = float(to_time_str.split(':')[0]) + float(to_time_str.split(':')[1]) / 60

        return res

    @api.model
    def cron_demo_method(self):
        self.send_slots_report()

    def send_slots_report(self):
        doctors = self.env['hr.employee'].search([])
        for doctor in doctors:
            if doctor.slots_ids and any(
                    rec.date == date.today() and rec.booking_button == True for rec in doctor.slots_ids):
                template = self.env.ref('doctors_app.email_template_id_doctors')
                email_values = {
                    'email_to': doctor.work_email,
                }
                template.send_mail(doctor.id, email_values=email_values)

    def open_booked_slots_doctor(self):
        view_id = self.env.ref('doctors_app.view_booked_slots_form_doctors').id
        action_id = self.env.ref('doctors_app.action_booked_slots_doctor').id
        today = date.today()
        slot_data = self.env['doctor.time.slots'].search([
            ('doctor_id', '=', self.id),
            ('date', '=', today),
            ('booking_button', '=', True)
        ])

        # Collect partner IDs from the slot_data recordset (assuming 'partner_ids' is a Many2many field)
        partner_ids = slot_data.mapped('partner_ids').ids

        context = dict(self.env.context)
        context.update({
            'default_doctor_id': self.id,
            'default_partner_ids': [(6, 0, partner_ids)],  # Pass the list of partner IDs using [(6, 0, ids)]
        })

        return {
            'name': 'Booked Slots',
            'type': 'ir.actions.act_window',
            'res_model': 'doctor.time.slots',
            'view_mode': 'tree',
            'views': [(view_id, 'tree')],
            'target': 'new',
            'domain': [('id', 'in', slot_data.ids)],
            'context': context,
            'action': action_id,
        }

    # def open_booked_slots_doctor(self):
    #     view_id = self.env.ref('doctors_app.view_booked_slots_form_doctors').id
    #     action_id = self.env.ref('doctors_app.action_booked_slots_doctor').id
    #     today = date.today()
    #     slot_data = self.env['doctor.time.slots'].search([
    #      ('doctor_id', '=', self.id),
    #      ('date', '=', today),
    #      ('booking_button', '=', True)])
    #     context = dict(self.env.context)
    #     context.update({
    #         'default_doctor_id': self.id,
    #         'default_slots': slot_data.ids,
    #     })
    #     return {
    #         'name': 'Booked Slots',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'doctor.time.slots',
    #         'view_mode': 'tree',
    #         'views': [(view_id, 'tree')],
    #         'target': 'new',
    #         'domain': [('id', 'in', slot_data.ids)],
    #         'context': context,
    #         'action': action_id,
    #     }


    def create_zoom_meeting(self):
        api_key = "EKgsBRIxS6nkvGfMnnH1w"
        api_secret = "N1CB2uRMKB9jyaO35kQ5lxt50M0MqtAH"

        # API endpoints
        base_url = "https://api.zoom.us/v2"
        meeting_create_url = f"{base_url}/users/me/meetings"

        # Create a meeting
        headers = {
            "Authorization": f"Bearer {api_key}:{api_secret}",
            "Content-Type": "application/json"
        }

        payload = {
            "topic": "My Zoom Meeting",
            "type": 2,  # Scheduled meeting
            "start_time": "2023-06-20T09:00:00",
            "duration": 60,
            "timezone": "America/New_York"
        }

        response = requests.post(meeting_create_url, headers=headers, data=json.dumps(payload))
        data = response.json()

        # Handle the response
        if response.status_code == 201:
            meeting_id = data["id"]
            booking = self.env['booking.model'].browse(self.env.context.get('active_id'))
            booking.zoom_meeting_id = meeting_id
            join_url = data["join_url"]
            booking.meeting_link = join_url
            print(f"Meeting created! ID: {meeting_id}, Join URL: {join_url}")
        else:
         print("Failed to create the meeting.")
         print(f"Error: {data['message']}")

