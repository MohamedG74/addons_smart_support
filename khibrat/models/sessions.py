from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri
from odoo.exceptions import ValidationError

class Sessions(models.Model):
    _name = "sessions.data"


    sessions=fields.Selection([('session_1','الجلسة الاولى'),
                            ('session_2','الجلسة الثانية'),
                            ('session_3','الجلسة الثالثة'),
                            ('session_4','الجلسة الرابعة'),
                            ('session_5','الجلسة الخامسة'),
                            ('session_6','الجلسة السادسة'),
                            ('session_7','الجلسة السابعة'),
                            ('session_8','الجلسة الثامنة'),
                            ('session_9','الجلسة التاسعة'),
                            ('session_10','الجلسة العاشرة')],string="الجلسات")
    
    session_number=fields.Char(string="رقم الجلسة", required = True)
    
    session_date=fields.Date(string="تاريخ الجلسة")
    session_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_session_date_hijri",readonly=True)
    
    session_will_be_held=fields.Selection([('offline','حضورى'),
                                           ('online','عن بعد')], string="كيفية إنعقادها")
    
    # session_clients=fields.Many2one('clients.data',string="المُدعى")
    # session_defendants=fields.Many2one('defendant.data',string="المُدعى عليه")

    session_clients=fields.One2many('clients.data', 'client_id', related = 'case_id.client_ids', string="المُدعى", readonly=True)
    session_many2many_clients=fields.Many2many('clients.data',related = 'case_id.client_many2many_ids', string="المُدعى", readonly=True)
    
    session_defendants=fields.One2many('defendant.data','defendant_id', related='case_id.defendant_ids',string="المُدعى عليه", readonly=True)
    session_many2many_defendants=fields.Many2many('defendant.data',related='case_id.defendant_many2many_ids',string="المُدعى عليه", readonly=True)

    session_interfering_related=fields.One2many('interfering.data','interfering_id', related='case_id.interfering_ids',string="متدخلين")
    session_many2many_interfering_related=fields.Many2many('interfering.data', related='case_id.interfering_many2many_ids',string="متدخلين")
    
    session_entries_related=fields.One2many('entries.data','entries_id', related='case_id.entries_ids',string="مدخلين")
    session_many2many_entries_related=fields.Many2many('entries.data', related='case_id.entries_many2many_ids',string="مدخلين")
    
    
    
    session_others=fields.Selection([('other_exist','اخرون'),
                                    ('other_not_exist','لا يوجد اخرون'),], default='other_not_exist',string="اخرون")
    
    session_experts=fields.Many2many('experts.data',string="خبراء")
    session_witness=fields.Many2many('witness.data',string="شهود")


    session_report=fields.Char(string="محضرها")
    session_conclusion=fields.Char(string="موجز وقائعها")
    required_for_next_session=fields.Text(string="المطلوب بالجلسة القادمة")

    next_session_date=fields.Date(string="تاريخ الجلسة القادمة")
    next_session_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_next_session_date_hijri",readonly=True)

    session_notes=fields.Char(string="ملاحظات وتوصيات")
    session_decision=fields.Selection([('session_decision_1','شطب الدعوى'),
                                       ('session_decision_2','قرار اخر'),], default='session_decision_1',string="القرار الصادر فيها")

    lawyers_attendees=fields.Many2many('lawyers.data',string='المحامون الحاضرون بالجلسة')

    case_id=fields.Many2one('cases.data',string='رقم الدعوى')
    
    stage_in_sessions=fields.Char(string='المرحلة')

    reservation_ids=fields.One2many('reservation.data','reservation_id',string='Reservationsss')

    another_decision_ids=fields.One2many('another.decision','another_decision_id',string='القرار')
    
    session_report_ids=fields.One2many('session.report','session_report_id',string='تقرير الجلسة')

    @api.onchange('session_date')
    def _compute_session_date_hijri(self):
        for rec in self:
            if rec.session_date:
                rec.session_date_hijri = Gregorian.fromdate(rec.session_date).to_hijri()
            else:
                rec.session_date_hijri = Hijri.today()
    
    @api.onchange('next_session_date')
    def _compute_next_session_date_hijri(self):
        for rec in self:
            if rec.next_session_date:
                rec.next_session_date_hijri = Gregorian.fromdate(rec.next_session_date).to_hijri()
            else:
                rec.next_session_date_hijri = Hijri.today()


    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.session_number)))
        return res



    def action_session(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الجلسة',
            'view_mode': 'form',
            'res_model': 'sessions.data',
            'res_id': self.id,
            # 'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False}"
        }
    

    def action_add_decision(self):
        return {
            'name':'إضافة قرار',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'another.decision',
            'context': {'default_case_id': self.case_id.id, 'default_another_decision_id': self.id},
            # 'target': 'new'
        }
    
    def action_add_session_report(self):
        return {
            'name':'إضافة تقرير الجلسة',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'session.report',
            'context': {'default_case_id_report': self.case_id.id, 'default_session_report_id': self.id},
        }
    

    # @api.onchange('sessions')
    # def _onchange_session_number(self):
    #     for rec in self:
    #         if rec.sessions or rec.sessions and  not rec.session_report_ids:
    #             raise ValidationError(_("برجاء إدخال تقرير الجلسة"))
    #     return {
    #         'warning': {
    #             'title': 'Warning!',
    #             'message': 'برجاء إدخال تقرير الجلسة'}
    #     }