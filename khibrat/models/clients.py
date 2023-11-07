from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class lawyers(models.Model):
    _name = "clients.data"

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

    #اسم المدير في السجل التجارى
    commerial_register_manager = fields.Char(string="اسم المدير في السجل التجارى")

    
    client_id=fields.Many2one('cases.data',string='Client')

    #field in clients to get data from cases.data and show it in the mail template
    client_idss=fields.Many2many('cases.data',string='Client')


    lawyer_ids=fields.One2many('lawyers.data', 'lawyerssss_id', string="المحامون")
    consultant_ids=fields.One2many('consultants.data', 'consultant_id', string="المستشارون")

    lawyer_many2many_ids=fields.Many2many('lawyers.data', string="المحامون")
    consultant_many2many_ids=fields.Many2many('consultants.data', string="المستشارون")


    #الوكالة Agency
    document_name_lawyer=fields.Char(string="اسم المستند")
    document_file_lawyer= fields.Binary(string="مستند الوكالة لدى المحامين")
    agency_ended_date_lawyer = fields.Date(string="تاريخ إنتهاء الوكالة لدى المحامين")
    agency_ended_date_hijri_lawyer = fields.Char(string="التاريخ الهجري", compute="_compute_agency_ended_date_hijri",readonly=True)
    
    
    document_name_consultant=fields.Char(string="اسم المستند")
    document_file_consultant= fields.Binary(string="مستند الوكالة لدى المستشارين")
    agency_ended_date_consultant = fields.Date(string="تاريخ إنتهاء الوكالة لدى المستشارين")
    agency_ended_date_hijri_consultant = fields.Char(string="التاريخ الهجري", compute="_compute_ended_date_hijri_consultant",readonly=True)


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


    @api.onchange('agency_ended_date_lawyer')
    def _compute_agency_ended_date_hijri(self):
        for rec in self:
            if rec.agency_ended_date_lawyer:
                rec.agency_ended_date_hijri_lawyer = Gregorian.fromdate(rec.agency_ended_date_lawyer).to_hijri()
            else:
                rec.agency_ended_date_hijri_lawyer = Hijri.today()
    
    @api.onchange('agency_ended_date_consultant')
    def _compute_ended_date_hijri_consultant(self):
        for rec in self:
            if rec.agency_ended_date_consultant:
                rec.agency_ended_date_hijri_consultant = Gregorian.fromdate(rec.agency_ended_date_consultant).to_hijri()
            else:
                rec.agency_ended_date_hijri_consultant = Hijri.today()


    def action_client(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'المُدعى',
            'view_mode': 'form',
            'res_model': 'clients.data',
            'res_id': self.id,
            'context': "{'create': False}"
        }   
    

    