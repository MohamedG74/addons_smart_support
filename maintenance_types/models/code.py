from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Code(models.Model):
    _name = "code.data"
    _description= "code"
    

    code = fields.Char(string="Location Code")
    gregorian_date=fields.Date(string="التاريخ الميلادي")

    hijri_date = fields.Char(string="التاريخ الهجري",compute="_compute_hijri_date",readonly=True)

    day_name=fields.Char(string="test")
    
    @api.onchange('gregorian_date')
    def _compute_hijri_date(self):
        for rec in self:
            if rec.gregorian_date:
                rec.hijri_date = Gregorian.fromdate(rec.gregorian_date).to_hijri()
                # rec.day_name = Gregorian.day_name(rec.gregorian_date)
            else:
                rec.hijri_date = Hijri.today()
        
    
    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.code)))
        return res    