from odoo import api, fields, models, _

class Court(models.Model):
    _name = "court.types"
    
    court_name = fields.Char(string="الجهة القضائية")    
    court_type = fields.Char(string="نوع الجهة القضائية")    
