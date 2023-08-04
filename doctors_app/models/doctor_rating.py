from odoo import models, fields, api


class DoctorRating(models.Model):
    _name = 'doctor.rating'
    _description = 'Doctor Rating'

    doctor_id = fields.Many2one('hr.employee', string='Doctor', ondelete='cascade')
    patient_ids = fields.Many2many('res.partner', string='Patient')
    rating = fields.Float(string='Rating', default=0.0)
    count = fields.Integer(string='Count', default=0)

    @api.onchange('rating', 'count')
    def _onchange_rating(self):
        if self.count > 0:
            self.rating = self.rating / self.count
        else:
            self.rating = 0.0

    def _compute_average_rating(self):
        for rating in self:
            if rating.count > 0:
                rating.rating = rating.rating / rating.count
            else:
                rating.rating = 0.0

    @api.model
    def _clean_duplicate_ratings(self):
        doctors = self.env['hr.employee'].search([])
        for doctor in doctors:
            ratings = self.env['doctor.rating'].search([('doctor_id', '=', doctor.id)], order='id desc')
            if len(ratings) > 1:
                # Keep the latest rating and delete the rest
                ratings_to_delete = ratings[1:]
                ratings_to_delete.unlink()

    def write(self, vals):
        if 'rating' in vals or 'count' in vals:
            self._onchange_rating()
        # Before writing new data, clean up duplicates
        self._clean_duplicate_ratings()
        return super(DoctorRating, self).write(vals)

    @api.model_create_single
    def create(self, vals_list):
        if vals_list.get('rating') or vals_list.get('count'):
            vals_list['rating'] = vals_list['rating'] / vals_list['count']
        # Before creating new data, clean up duplicates
        self._clean_duplicate_ratings()
        return super(DoctorRating, self).create(vals_list)
