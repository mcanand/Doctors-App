from odoo import fields, models
import datetime

class DoctorPatientPrescription(models.Model):
    _name = 'doctor.patient.prescription'
    _description = 'Doctor Patient Prescription'

    name = fields.Char(string='Name')
    department_id = fields.Many2one('hr.department', string='Department')
    case_details = fields.Text(string='Case Details')
    prescription = fields.Text(string='Prescription')
    slot_id = fields.Many2one('doctor.time.slots', string='Time Slot', ondelete='cascade')
    partner_ids = fields.Many2many('res.partner', string='Patient')
    doctor_id = fields.Many2one('hr.employee', string='Doctor', store=True)
    next_visit = fields.Date(string='Next Visit')
    date = fields.Date(string='Date')
    lab_attachment = fields.Many2many('lab.attachment', string='Lab Attachment')


    def rate_doctor(self):
        selected_partner = self.partner_ids[0]
        action = self.env.ref('doctors_app.action_doctor_rating').read()[0]
        action['context'] = {
            'default_doctor_id': self.doctor_id.id,
            'default_patient_ids': [(6, 0, [selected_partner.id])],
        }
        return action

    def view_available_dates(self):
        current_date = datetime.date.today()
        available_dates = self.env['doctor.time.slots'].search([
            ('date', '>=', current_date),
            ('booking_button', '=', False)
        ]).mapped('date')
        action = self.env.ref('doctors_app.action_view_available_dates').read()[0]
        action['domain'] = [('id', 'in', self.ids)]
        action['context'] = {
            'res_model': 'doctor.time.slots',
            'view_mode': 'tree',
            'view_id': self.env.ref('doctors_app.view_available_dates').id,

        }
        return action


