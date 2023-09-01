from odoo import models, fields, api

class DoctorRating(models.Model):
    _name = 'doctor.rating'
    _description = 'Doctor Rating'

    doctor_id = fields.Many2one('hr.employee', string='Doctor', ondelete='cascade')
    patient_ids = fields.Many2many('res.partner', string='Patient')
    rating = fields.Float(string='Rating', default=0.0)
    count = fields.Integer(string='Count', default=0)

    @api.model_create_single
    def create(self, vals_list):
        if 'rating' in vals_list and 'doctor_id' in vals_list:
            # Check if a rating already exists for the same doctor
            existing_rating = self.search([
                ('doctor_id', '=', vals_list['doctor_id']),
            ], limit=1)

            if existing_rating:
                # If a rating already exists, update the count and recalculate the rating
                existing_rating.rating = (existing_rating.rating * existing_rating.count + vals_list['rating']) / (
                            existing_rating.count + 1)
                existing_rating.count += 1
                return existing_rating
            else:
                # If no rating exists for the doctor, create a new one
                vals_list['count'] = 1
                return super(DoctorRating, self).create(vals_list)
        else:
            return super(DoctorRating, self).create(vals_list)

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
        # Before writing new data, clean up duplicates
        self._clean_duplicate_ratings()
        return super(DoctorRating, self).write(vals)
