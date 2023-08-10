from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from zoomus import ZoomClient


class Doctor(models.Model):
    _name = 'doctor.time.slots'
    _description = 'Doctor Time Slots'

    doctor_id = fields.Many2one('hr.employee', string='Doctor')
    partner_ids = fields.Many2many('res.partner', string='Partner', default=False)
    display_time_interval = fields.Char(string='Time Interval')
    booking_button = fields.Boolean(string='Assigned', default=False)
    time_from = fields.Float(string='From', related='doctor_id.time_from', readonly=True)
    time_to = fields.Float(string='To', related='doctor_id.time_to', readonly=True)
    date = fields.Date(default=lambda self: datetime.now().date() + timedelta(days=1))
    meeting_link = fields.Char(string='Meeting Link', store=True)
    booking_status = fields.Boolean(string='Completed', default=False)
    patient_prescription_ids = fields.One2many('doctor.patient.prescription', 'slot_id', string='Prescriptions')
    multiple_partners = fields.Boolean(string="Multiple Partners", compute="_compute_multiple_partners")
    from_time = fields.Char(string='Start Time', compute='_compute_from_time', store=True)
    to_time = fields.Char(string='End Time', compute='_compute_to_time', store=True)
    group_meeting = fields.Char(string='Session Name', store=True)
    prescription_status = fields.Boolean(string='Prescription Completed', compute='_compute_prescription_status',
                                         store=True)


    @api.depends('patient_prescription_ids.prescription_status')
    def _compute_prescription_status(self):
        for slot in self:
            slot.prescription_status = any(
                prescription.prescription_status for prescription in slot.patient_prescription_ids)


    @api.depends('partner_ids')
    def _compute_multiple_partners(self):
        for slot in self:
            slot.multiple_partners = len(slot.partner_ids) > 1



    def view_prescription(self):
        prescription = self.patient_prescription_ids[0] if self.patient_prescription_ids else False

        if not prescription:
            prescription = self.env['doctor.patient.prescription'].create({
                'slot_id': self.id,
                'partner_ids': [(6, 0, self.partner_ids.ids)],  # Set Many2many field using [(6, 0, ids)]
                'doctor_id': self.doctor_id.id,
                'date': self.date,
                'department_id': self.doctor_id.department_id.id,
            })

        prescription.update({
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

    # def view_prescription(self):
    #     if self.patient_prescription_ids:
    #         prescription = self.patient_prescription_ids[0]
    #     else:
    #         prescription = self.env['doctor.patient.prescription'].create({
    #             'slot_id': self.id,
    #             'partner_ids': self.partner_ids.id,
    #             'doctor_id': self.doctor_id.id,
    #             'date': self.date,
    #         })
    #     prescription.update({
    #         'department_id': self.doctor_id.department_id.id,
    #         'doctor_id': self.doctor_id.id,
    #         'date': self.date,
    #     })
    #
    #     prescription_view = self.env.ref('doctors_app.view_prescription_form')
    #     return {
    #         'name': 'Prescription',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'doctor.patient.prescription',
    #         'res_id': prescription.id,
    #         'view_id': prescription_view.id,
    #         'type': 'ir.actions.act_window',
    #     }


    # Set boolean button true and assign meeting link while booking
    @api.onchange('partner_ids')
    def on_partner_id_change(self):
        if self.partner_ids:
            self.booking_button = True
            self.meeting_link="/gggggg/nnnnnnnnn"
        else:
            self.booking_button = False



    # booking validation
    @api.constrains('doctor_id', 'date', 'from_time', 'to_time', 'partner_ids')
    def _check_unique_booking(self):
        for slot in self:
            if slot.date and slot.from_time and slot.to_time and slot.partner_ids:
                partner_ids = slot.partner_ids.ids
                if len(partner_ids) != len(set(partner_ids)):
                    raise ValidationError("Same partner cannot be added multiple times to the same time slot.")

    # @api.constrains('doctor_id', 'date', 'partner_ids')
    # def _check_unique_booking(self):
    #     for slot in self:
    #         if slot.date and slot.partner_ids:
    #             domain = [
    #                 ('id', '!=', slot.id),
    #                 ('doctor_id', '=', slot.doctor_id.id),
    #                 ('date', '=', slot.date),
    #                 ('partner_ids', 'in', slot.partner_ids.ids),
    #                 # Check if any of the selected partners exist in the list
    #             ]
    #             existing_slots = self.search(domain)
    #             if existing_slots:
    #                 raise ValidationError(
    #                     "One or more of the selected partners have already booked this doctor for the selected date.")



