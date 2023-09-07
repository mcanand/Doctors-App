from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import date, datetime, timedelta
import logging

_logger = logging.getLogger(__name__)


class Doctor(models.Model):
    _inherit = 'hr.employee'

    date = fields.Date(default=lambda self: datetime.now().date() + timedelta(days=1))
    time_from = fields.Float(string='From(24 hour format)')
    time_to = fields.Float(string='To(24 hour format)')
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
    work_address = fields.Text(string='Work Address Details')
    CATEGORY_SELECTION = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    cate_id = fields.Selection(CATEGORY_SELECTION, string='Category')
    HOLIDAY_SELECTION = [
        ('6', 'Sunday'),
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
    ]

    holiday1 = fields.Selection(HOLIDAY_SELECTION, string='Holiday 1')
    holiday2 = fields.Selection(HOLIDAY_SELECTION, string='Holiday 2')
    one_hour_fee = fields.Float(string='Sitting fee per hour', digits=(10, 2), default=0.0)
    ratings = fields.One2many('doctor.rating', 'doctor_id', string='Ratings')

    @api.model_create_multi
    def create(self, vals_list):
        res = super(Doctor, self).create(vals_list)

        for record_vals, record in zip(vals_list, res):
            if record_vals.get('time_from') is not None and record_vals.get('time_to') is not None:
                if record_vals['time_from'] > record_vals['time_to']:
                    raise ValidationError("Invalid time interval: time_from should be less than time_to")

                intervals = record._get_time_intervals(record_vals.get('time_from'), record_vals.get('time_to'))
                current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                end_date = current_date + timedelta(days=15)

                while current_date <= end_date:
                    # Check if the current day is a holiday
                    is_holiday = current_date.weekday() in (
                        int(record_vals.get('holiday1')), int(record_vals.get('holiday2')))

                    # If it's not a holiday, create slots
                    if not is_holiday:
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

        if any(field_name in vals for field_name in ('time_from', 'time_to', 'date',)):
            for doctor in self:
                if doctor.time_from and doctor.time_to and doctor.date:
                    if doctor.time_from > doctor.time_to:
                        raise ValidationError("Invalid time interval: time_from should be less than time_to")

                    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(
                        days=1)
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
                        print(f"current_date.weekday(): {current_date.weekday()}")
                        print(f"holiday1: {doctor.holiday1}")
                        # print(f"doctor.holiday2: {doctor.holiday2}")

                        # Check if the current day is either holiday1 or holiday2
                        is_holiday = (
                                current_date.weekday() == int(doctor.holiday1) or current_date.weekday() == int(
                            doctor.holiday2))
                        print(is_holiday)

                        # If it's not a holiday, create slots
                        if not is_holiday:
                            # if current_date.weekday() not in (doctor.holiday1, doctor.holiday2):
                            for from_time, to_time in intervals:
                                display_interval = f'From {from_time} to {to_time}'
                                self.env['doctor.time.slots'].create({
                                    'doctor_id': doctor.id,
                                    'partner_ids': [(6, 0, doctor.partner_ids.ids)],
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

    # def write(self, vals):
    #     res = super(Doctor, self).write(vals)
    #
    #     if any(field_name in vals for field_name in ('time_from', 'time_to', 'date', 'holiday1', 'holiday2')):
    #         for doctor in self:
    #             if doctor.time_from and doctor.time_to and doctor.date:
    #                 if doctor.time_from > doctor.time_to:
    #                     raise ValidationError("Invalid time interval: time_from should be less than time_to")
    #
    #                 start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    #                 end_date = start_date + timedelta(days=15)
    #
    #                 slots = self.env['doctor.time.slots'].search([
    #                     ('doctor_id', '=', doctor.id),
    #                     ('date', '>=', start_date.strftime("%Y-%m-%d")),
    #                     ('date', '<=', end_date.strftime("%Y-%m-%d"))
    #                 ])
    #
    #                 # Remove existing slots
    #                 slots.unlink()
    #
    #                 # Generate new slots
    #                 current_date = start_date
    #
    #                 while current_date <= end_date:
    #                     if current_date.weekday() not in (doctor.holiday1,doctor.holiday2):
    #                         print(doctor.holiday1)
    #                         intervals = doctor._get_time_intervals(doctor.time_from, doctor.time_to)
    #                         for from_time, to_time in intervals:
    #                             display_interval = f'From {from_time} to {to_time}'
    #                             self.env['doctor.time.slots'].create({
    #                                 'doctor_id': doctor.id,
    #                                 'partner_ids': [(6, 0, doctor.partner_ids.ids)],
    #                                 'date': current_date.strftime("%Y-%m-%d"),
    #                                 'from_time': from_time,
    #                                 'to_time': to_time,
    #                                 'display_time_interval': display_interval,
    #                             })
    #                     current_date += timedelta(days=1)
    #
    #     if 'display_time_interval' in vals:
    #         for doctor in self:
    #             # Extract 'from_time' and 'to_time' from the 'display_time_interval' when it's being updated
    #             from_time_str, to_time_str = vals.get('display_time_interval', '').split(' to ')
    #             doctor.time_from = float(from_time_str.split(':')[0]) + float(from_time_str.split(':')[1]) / 60
    #             doctor.time_to = float(to_time_str.split(':')[0]) + float(to_time_str.split(':')[1]) / 60
    #
    #     return res

    @api.model
    def create_slots_for_all_doctors(self):
        # Get all doctor records
        doctors = self.env['hr.employee'].search([])
        for doctor in doctors:
            doctor.create_slots_without_weekends()

    def create_slots_without_weekends(self):
        current_date = fields.Date.today()
        date_to_check = current_date + timedelta(days=1)

        # Check if slots already exist after 1 day
        existing_slots = self.env['doctor.time.slots'].search([
            ('doctor_id', '=', self.id),
            ('date', '=', date_to_check.strftime("%Y-%m-%d")),
            ('from_time', '>=', self.time_from),
            ('to_time', '<=', self.time_to),
        ])

        if not existing_slots and self.time_from and self.time_to:
            # No slots found after 1 day, so create slots for the next 15 days
            dates = []
            for i in range(15):
                dates.append(date_to_check + timedelta(days=i))

            for current_date in dates:
                intervals = self._get_time_intervals(self.time_from, self.time_to)
                print(f"current_date.weekday(): {current_date.weekday()}")
                print(f"holiday1: {self.holiday1}")
                is_holiday = (
                        current_date.weekday() == int(self.holiday1) or current_date.weekday() == int(
                    self.holiday2))
                print(is_holiday)

                # If it's not a holiday, create slots
                if not is_holiday:
                    # if current_date.we
                    # Create slots for weekdays

                    for from_time, to_time in intervals:
                        display_interval = f'From {from_time} to {to_time}'
                        # Check if there are no existing slots that overlap
                        existing_overlapping_slots = self.env['doctor.time.slots'].search([
                            ('doctor_id', '=', self.id),
                            ('date', '=', current_date.strftime("%Y-%m-%d")),
                            ('from_time', '<=', to_time),
                            ('to_time', '>=', from_time),
                        ])
                        if not existing_overlapping_slots:
                            self.env['doctor.time.slots'].create({
                                'doctor_id': self.id,
                                'partner_ids': [(6, 0, self.partner_ids.ids)],
                                'date': current_date.strftime("%Y-%m-%d"),
                                'from_time': from_time,
                                'to_time': to_time,
                                'display_time_interval': display_interval,
                            })

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

        # Collect partner IDs from the slot_data recordset
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

    def open_all_slots(self):
        view_id = self.env.ref('doctors_app.view_all_slots_form').id
        action_id = self.env.ref('doctors_app.action_all_slots').id
        today = date.today()
        slot_data = self.env['doctor.time.slots'].search([
            ('doctor_id', '=', self.id),
            # ('date', '>=', today),
        ])
        context = dict(self.env.context)
        context.update({
            'default_doctor_id': self.id,
            'default_slots': slot_data.ids,
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
