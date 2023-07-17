from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from zoomus import ZoomClient


class Doctor(models.Model):
    _name = 'doctor.time.slots'
    _description = 'Doctor Time Slots'

    doctor_id = fields.Many2one('hr.employee', string='Doctor')
    partner_id = fields.Many2one('res.partner', string='Partner', default=False)
    display_time_interval = fields.Char(string='Time Interval')
    booking_button = fields.Boolean(string='Assigned', default=False)
    time_from = fields.Float(string='From', related='doctor_id.time_from', readonly=True)
    time_to = fields.Float(string='To', related='doctor_id.time_to', readonly=True)
    date = fields.Date(default=lambda self: datetime.now().date() + timedelta(days=1))
    meeting_link = fields.Char(string='Meeting Link', store=True)
    booking_status = fields.Boolean(string='Completed', default=False)
    patient_prescription_ids = fields.One2many('doctor.patient.prescription', 'slot_id', string='Prescriptions')

    def view_prescription(self):
        if self.patient_prescription_ids:
            prescription = self.patient_prescription_ids[0]
        else:
            prescription = self.env['doctor.patient.prescription'].create({
                'slot_id': self.id,
                'partner_id': self.partner_id.id,
                'doctor_id': self.doctor_id.id,
                'date': self.date,
            })
        prescription.update({
            'department_id': self.doctor_id.department_id.id,
            'doctor_id': self.doctor_id.id,
            'date': self.date,
        })

        prescription_view = self.env.ref('doctors_app.view_prescription_form')
        return {
            'name': 'Prescription',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'doctor.patient.prescription',
            'res_id': prescription.id,
            'view_id': prescription_view.id,
            'type': 'ir.actions.act_window',
        }


    # Set boolean button true and assign meeting link while booking
    @api.onchange('partner_id')
    def on_partner_id_change(self):
        if self.partner_id:
            self.booking_button = True
            self.meeting_link="/gggggg/nnnnnnnnn"
        else:
            self.booking_button = False


    # booking validation
    @api.constrains('doctor_id', 'date', 'partner_id')
    def _check_unique_booking(self):
        for slot in self:
            if slot.date and slot.partner_id:
                domain = [
                    ('id', '!=', slot.id),
                    ('doctor_id', '=', slot.doctor_id.id),
                    ('date', '=', slot.date),
                    ('partner_id', '=', slot.partner_id.id),
                ]
                existing_slots = self.search(domain)
                if existing_slots:
                    raise ValidationError("The partner has already booked this doctor for the selected date.")

