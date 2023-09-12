from odoo import models, fields

class DoctorReview(models.Model):
    _name = 'doctor.review'
    _description = 'Doctor Review'

    doctor_id = fields.Many2one('hr.employee', string='Doctor', required=True)
    patient_id = fields.Many2one('res.partner', string='Patient', required=True)

    review_text = fields.Text(string='Review', required=True)
    rating_id = fields.Many2one('doctor.rating', string='Doctor Rating')
