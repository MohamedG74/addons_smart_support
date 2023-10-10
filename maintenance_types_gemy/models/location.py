from odoo import api,fields,models

class Mainlocations(models.Model):
    _name='main.location'
    _describtion='Maintenance Locations'


    ##fields
    id_=fields.Integer(string="ID")
    name=fields.Char(string="Name")
    location_code=fields.Char(string="Location Code")
    address=fields.Text(string="Address")
    type_=fields.Char(string="Type")
    classify=fields.Selection([('external', 'External'),('internal','Internal')],string="Classifacation")

