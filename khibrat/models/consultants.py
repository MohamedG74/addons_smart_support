from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Consultants(models.Model):
    _name = "consultants.data"

    name = fields.Char(string="الاسم")
    
    identity_card = fields.Selection([('national_id','رقم الهوية'),('passport','جواز سفر')], string="اثبات الشخصية")
    identity_card_number = fields.Char(string="رقم اثبات الشخصية")
    address = fields.Char(string="العنوان")
    email=fields.Char(string="البريد الإلكترونى")
    
    published_date = fields.Date(string="تاريخ الصدور")
    published_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_published_date_hijri",readonly=True)

    ended_date = fields.Date(string="تاريخ الانتهاء")
    ended_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_ended_date_hijri",readonly=True)

    phone_number = fields.Char(string="رقم الهاتف")
    notes = fields.Text(string="ملاحظات")
    commerial_register = fields.Char(string="رقم السجل التجارى")

    commerial_register_start_date = fields.Date(string="تاريخ صدور السجل التجارى")
    commerial_register_start_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_start_date_hijri",readonly=True)

    commerial_register_end_date = fields.Date(string="تاريخ إنتهاء السجل التجارى")
    commerial_register_end_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_end_date_hijri",readonly=True)

    commerial_register_manager = fields.Char(string="اسم المدير في السجل التجارى")

    consultant_id=fields.Many2one('clients.data',string='Consultant')
    consultant_id_defendant=fields.Many2one('defendant.data',string='Consultant')


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
    
    @api.onchange('commerial_register_start_date')
    def _compute_commerial_register_start_date_hijri(self):
        for rec in self:
            if rec.commerial_register_start_date:
                rec.commerial_register_start_date_hijri = Gregorian.fromdate(rec.commerial_register_start_date).to_hijri()
            else:
                rec.commerial_register_start_date_hijri = Hijri.today()
    
    @api.onchange('commerial_register_end_date')
    def _compute_commerial_register_end_date_hijri(self):
        for rec in self:
            if rec.commerial_register_end_date:
                rec.commerial_register_end_date_hijri = Gregorian.fromdate(rec.commerial_register_end_date).to_hijri()
            else:
                rec.commerial_register_end_date_hijri = Hijri.today()
