from odoo import models, fields, api
from odoo.exceptions import UserError,ValidationError


class Doctor(models.Model):
    _name = 'doctor.details'
    _description = 'Doctor Details'

    name = fields.Char(string='Name', required=True)
    department_id = fields.Many2one('hr.department', string='Department')
    email = fields.Char(string='Email')
    date_of_birth = fields.Date(string='Date of Birth')
    experience = fields.Integer(string='Experience (in years)')
    certificates = fields.Many2many('doctor.certificate', string='Certificates')
    work_address = fields.Text(string='Work Address')
    mobile = fields.Char(string='Mobile')
    about = fields.Text(string='About')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    user_id = fields.Many2one('res.users', string='User')
    partner_ids = fields.Many2many('res.partner', string='Partner')
    private_contact_address = fields.Text(string='Private Contact Address')
    state_id = fields.Many2one('res.country.state', string='State' , domain="[('country_id.code', '=', 'IN')]")
    emergency_contact_name = fields.Char(string='Emergency Contact Name')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone')
    # Education
    certificate_level = fields.Char(string='Certificate Level')
    field_of_study = fields.Char(string='Field of Study')
    status = fields.Selection(
        [('1', 'Approved'), ('2', 'Pending'), ('3', 'Rejected')],
        string='Status',
        default='2'  # Set default status as 'Pending'
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender'
    )
    stage = fields.Selection(
        [('approved', 'Approved'), ('rejected', 'Rejected')],
        string='Stage',
        compute='_compute_stage',
        store=True
    )
    profile_pic = fields.Binary(string='Profile Picture', attachment=True)
    # date = fields.Date(default=lambda self: datetime.now().date() + timedelta(days=1))
    time_from = fields.Char(string='From')
    time_to = fields.Char(string='To')


    @api.depends('status')
    def _compute_stage(self):
        for record in self:
            if record.status == '1':
                record.stage = 'approved'
            elif record.status == '3':
                record.stage = 'rejected'
            else:
                record.stage = ''




    def action_approve(self):
        self.status = '1'
        self.create_user()
        return


    def action_rejected(self):
        self.status = '3'
        return

    def create_user(self):
        Users = self.env['res.users']
        for doctor in self:
         user_vals = {
            'name': doctor.name,
            'login': doctor.email,
            'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])]
         }
        try:
            user = Users.create(user_vals)
        except ValidationError:
            raise UserError(("The user cannot be created. Please check the user information."))

        # #  ate res.partner record
        user.partner_id.write({'name': doctor.name, 'email': doctor.email, 'user_id': user.id})
        # Create employee for user
        user.action_create_employee()
        time_from_str = doctor.time_from.replace(':', '.')
        time_to_str = doctor.time_to.replace(':', '.')

        # Update employee record
        user.employee_id.write({
            'name': doctor.name,
            'gender': doctor.gender,
            'department_id': doctor.department_id.id,
            'work_email': doctor.email,
            'work_address': doctor.work_address,
            'mobile_phone': doctor.mobile,
            'emergency_contact': doctor.emergency_contact_name,
            'emergency_phone': doctor.emergency_contact_phone,
            'cate_id': 'doctor',
            'time_from': time_from_str,
            'time_to': time_to_str,
        })
