{
    'name': 'Doctors App',
    'version': '1.0',
    'author': 'Anand',
    'category': 'Custom',
    'summary': 'Custom doctors app for managing patients and doctors',
    'depends': ['base', 'contacts', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/doctors_form_view.xml',
        'views/user_form_view.xml',
        'views/booked_slots.xml',
        'views/email_cron.xml',
        'views/email_template.xml',
        'views/patient_cron.xml',
        'views/patient_email.xml',
        'views/zoom_settings.xml',
        'views/booked_slots_doctor.xml',
        'views/doctor_prescription.xml',
        'views/patient_view_prescription.xml',
        'views/doctor_rating.xml',
        'views/available_dates.xml',
        'views/hr_department.xml',
        'views/doctor_details.xml',



    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
