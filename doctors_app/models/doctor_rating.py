from odoo import models, fields, api


class DoctorRating(models.Model):
    _name = 'doctor.rating'
    _description = 'Doctor Rating'

    doctor_id = fields.Many2one('hr.employee', string='Doctor')
    patient_id = fields.Many2one('res.partner', string='Patient')
    rating = fields.Integer(string='Rating', default=0)
    count = fields.Integer(string='Count', default=0)
    average_rating = fields.Float(string='Average Rating', compute='_compute_average_rating')

    @api.depends('rating', 'count')
    def _compute_average_rating(self):
        for rating in self:
            if rating.count > 0:
                rating.average_rating = rating.rating / rating.count
            else:
                rating.average_rating = 0.0