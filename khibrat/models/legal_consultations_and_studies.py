from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class legalconsultations(models.Model):
    _name = "legalconsultations.studies"
    _inherit = 'mail.thread'

    name = fields.Char(string="الاسم")
    phone_number = fields.Char(string="رقم الهاتف")
    email=fields.Char(string="البريد الإلكترونى")
    identity_card_number = fields.Char(string="رقم الهوية")
    commerial_register = fields.Char(string="رقم السجل التجارى")
    commerial_register_start_date = fields.Date(string="تاريخ صدور السجل التجارى")
    commerial_register_start_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_start_date_hijri",readonly=True)
    commerial_register_end_date = fields.Date(string="تاريخ إنتهاء السجل التجارى")
    commerial_register_end_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_commerial_register_end_date_hijri",readonly=True)
    commerial_register_manager = fields.Char(string="اسم المدير في السجل التجارى")
    

    consultation_request_date = fields.Date(string="تاريخ طلب الإستشارة")
    consultation_request_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_consultation_request_date_hijri",readonly=True)

    consultation_delivery_date = fields.Date(string="تاريخ تسليم الإستشارة")
    consultation_delivery_date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_consultation_delivery_date_hijri",readonly=True)

    
    consultation_type = fields.Selection([('x_1','إعداد لائحة دعوى'),('x_2','إعداد لائحة استئناف')
                                          ,('x_3','استشارات للشركات'),('x_4','استشارات للأفراد')
                                          ,('x_5','أخرى')], string="نوع الاستشارة")


    consultation_category_1 = fields.Selection([('إداري','إداري'), ('تجاري','تجاري'), ('أحوال شخصية','أحوال شخصية'),
                                                ('عمالي','عمالي'),('جنائي','جنائي'), ],string="تصنيف الاستشارة")
    
    consultation_category_2 = fields.Selection([('إداري','إداري'), ('تجاري','تجاري'), ('أحوال شخصية','أحوال شخصية'),
                                                ('عمالي','عمالي'),('جنائي','جنائي'), ],string="تصنيف الاستشارة")
    
    consultation_category_3 = fields.Selection([('إدارية','إدارية'), ('عمالية','عمالية'), ('تجارية','تجارية'),
                                                ('جنائية','جنائية'), ('أحوال شخصية','أحوال شخصية'), ('عقود','عقود'),
                                                ('رأي قانوني (أخري)','رأي قانوني (أخري)'),],string="تصنيف الاستشارة")
    
    consultation_category_4 = fields.Selection([('إدارية','إدارية'), ('عمالية','عمالية'), ('جنائية','جنائية'), 
                                                ('أحوال شخصية','أحوال شخصية'), ('عقود','عقود'),
                                                ('رأي قانوني (أخري)','رأي قانوني (أخري)'),], string="تصنيف الاستشارة")
    
    # list_lawsuit=fields.Binary(string="لائحة الدعوى")
    consultation_document = fields.Many2many('ir.attachment', string="المرفقات الخاصة بالاستشارة")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    consultation_fee=fields.Monetary(string="أتعاب الاستشارة", currency_field='company_currency_id')







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



    @api.onchange('consultation_request_date')
    def _compute_consultation_request_date_hijri(self):
        for rec in self:
            if rec.consultation_request_date:
                rec.consultation_request_date_hijri = Gregorian.fromdate(rec.consultation_request_date).to_hijri()
            else:
                rec.consultation_request_date_hijri = Hijri.today()
    
    @api.onchange('consultation_delivery_date')
    def _compute_consultation_delivery_date_hijri(self):
        for rec in self:
            if rec.consultation_delivery_date:
                rec.consultation_delivery_date_hijri = Gregorian.fromdate(rec.consultation_delivery_date).to_hijri()
            else:
                rec.consultation_delivery_date_hijri = Hijri.today()

