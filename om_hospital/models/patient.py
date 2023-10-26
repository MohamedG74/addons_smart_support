from odoo import api, fields, models

class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description= "patient_records"

    patient_name = fields.Char(string="Patient Name", required=True)
    disease_name = fields.Char(string="Disease Name", required=True)
    age = fields.Integer(string="Age")
    is_child = fields.Boolean(string="is_child ?")
    notes = fields.Text(string="Notes")
    gender = fields.Selection([('male', 'Male'),('female','Female'),('others','Others')],string="Gender")
    

#hospital.patient == hospital_patient


# from odoo import api, fields, models, _, tools
# class AccountAccount(models.Model):
#      _name = "account.account"