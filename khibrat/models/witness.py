from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Witness(models.Model):
    _name = "witness.data"

    name = fields.Char(string="الاسم")
    
    identity_card = fields.Selection([('national_id','رقم الهوية'),('passport','جواز سفر')], string="اثبات الشخصية")
    identity_card_number = fields.Char(string="رقم اثبات الشخصية")

    published_date = fields.Date(string="تاريخ الصدور")
    published_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_published_date_hijri",readonly=True)
    
    ended_date = fields.Date(string="تاريخ الانتهاء")
    ended_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_ended_date_hijri",readonly=True)
    
    phone_number = fields.Char(string="رقم الهاتف")
    notes = fields.Text(string="ملاحظات")

    @api.onchange('published_date')
    def _compute_published_date_hijri(self):
        for rec in self:
            if rec.published_date:
                rec.published_date_hijri = Gregorian.fromdate(rec.published_date).to_hijri()
            else:
                rec.published_date_hijri = Hijri.today()
    
    @api.onchange('ended_date')
    def _compute_ended_date_hijri(self):
        for rec in self:
            if rec.ended_date:
                rec.ended_date_hijri = Gregorian.fromdate(rec.ended_date).to_hijri()
            else:
                rec.ended_date_hijri = Hijri.today()