from odoo import models, fields, api
from datetime import date


class ResPartner(models.Model):
    _inherit = 'res.partner'

    CATEGORY_SELECTION = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    ]

    categry_id = fields.Selection(CATEGORY_SELECTION, string='Category', required=True)
    doctor_time_slot_ids = fields.One2many('doctor.time.slots', 'partner_id', string='Booked Slots')
    doctor_id = fields.Many2one('hr.employee', string='Doctor')
    date_of_birth = fields.Date(string='Date of Birth')







    def open_booked_slots(self):
        view_id = self.env.ref('doctors_app.view_booked_slots_form').id
        action_id = self.env.ref('doctors_app.action_booked_slots').id
        slot_data = self.env['doctor.time.slots'].search([('partner_id', '=', self.id)])
        context = dict(self.env.context)
        context.update({
            'default_partner_id': self.id,
            'default_slots': slot_data.ids,
        })
        return {
            'name': 'Booked Slots',
            'type': 'ir.actions.act_window',
            'res_model': 'doctor.time.slots',
            'view_mode': 'tree',
            'views': [(view_id, 'tree')],
            'target': 'new',
            'domain': [('partner_id', '=', self.id)],
            'context': context,
            'action': action_id,
        }

    def send_booking_reminder_email(self):
        patients = self.env['res.partner'].search([])
        for patient in patients:
            if patient.doctor_time_slot_ids:
                slots = []
                for rec in patient.doctor_time_slot_ids:
                    if rec.date == date.today():
                        slots.append(rec)
                if slots:
                    template = self.env.ref('doctors_app.email_template_id_patient')
                    email_values = {
                        'email_to': patient.email,
                    }
                    template.send_mail(patient.id, email_values=email_values)

    def view_prescription_details(self):
        prescriptions = self.env['doctor.patient.prescription'].search([('partner_id', '=', self.id)])

        action = self.env.ref('doctors_app.action_doctor_patient_prescription').read()[0]
        action.update({
            'domain': [('id', 'in', prescriptions.ids)],
            'context': {
                'default_partner_id': self.id,
            },
        })

        return action
