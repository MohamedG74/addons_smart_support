from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Interfering(models.Model):
    _name = "interfering.data"

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
    commerial_register = fields.Char(string="رقم السجل التجارى")

    commerial_register_start_date = fields.Date(string="تاريخ صدور السجل التجارى")
    commerial_register_start_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_start_date_hijri",readonly=True)

    commerial_register_end_date = fields.Date(string="تاريخ إنتهاء السجل التجارى")
    commerial_register_end_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_end_date_hijri",readonly=True)

    notes = fields.Text(string="ملاحظات")
    
    
    interfering_id=fields.Many2one('cases.data',string='Interfering')


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

    def action_interfering(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الجهة المتدخلة',
            'view_mode': 'form',
            'res_model': 'interfering.data',
            'res_id': self.id,
            'context': "{'create': False}"
        }   