from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri
import datetime

class Another_Decision(models.Model):
    _name = "another.decision"
    _rec_name= 'another_decision'
    
    another_decision=fields.Selection([('شطب الدعوى','شطب الدعوى'),
                                       ('تبادل مذكرات','تبادل مذكرات'),
                                       ('إجراء إحتياطى','إجراء إحتياطى'),
                                       ('إجراء إعدادى مرحلى','إجراء إعدادى مرحلى'),
                                       ('التأجيل','التأجيل'),] ,string="القرار الصادر فيها")
    # another_decision=fields.Selection([('شطب الدعوى','شطب الدعوى'),
    #                                    ('تبادل مذكرات','تبادل مذكرات'),
    #                                    ('إجراء إحتياطى','إجراء إحتياطى'),
    #                                    ('إجراء إعدادى مرحلى','إجراء إعدادي مرحلي'),
    #                                    ('التأجيل','التأجيل'),] ,string="القرار الصادر فيها")

    #تبادل مذكرات
    appointment = fields.Char(string="الموعد")
    phase = fields.Char(string="الجهة")
    date = fields.Date(string="التاريخ")
    date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_date_hijri",readonly=True)


    #إجراء إحتياطى
    procedure=fields.Selection([('x_1','إلقاء الحجز التحفظى'),
                                  ('x_2','المنع من التصرف'),
                                  ('x_3','المنع من السفر'),
                                  ('x_4','الحراسة القضائية')],string="إجراء إحتياطى")
    
    spoken=fields.Char(string="منطوق الإجراء")

    decision_date=fields.Date(string="تاريخ استلام صك القرار")
    decision_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_decision_date_hijri",readonly=True)

    last_date_for_resumption=fields.Date(string="تاريخ اخر موعد لإستئنافه")
    last_date_for_resumption_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_last_date_for_resumption_hijri",readonly=True)

    resupmtion=fields.Boolean(string="إستئنافه")
    registration_number=fields.Char(string="رقم القيد")

    registration_date=fields.Date(string="تاريخ القيد")
    registration_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_registration_date_hijri",readonly=True)

    resupmtion_circle=fields.Char(string="الدائرة الاستئنافية")
    resupmtion_verdict=fields.Char(string="الحكم الاستئنافى")
    resupmtion_verdict_number=fields.Char(string="رقم الاستئناف")

    resupmtion_verdict_date=fields.Date(string="تاريخ الاستئناف")
    resupmtion_verdict_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_resupmtion_verdict_date_hijri",readonly=True)

    resupmtion_verdict_spoken=fields.Char(string="منطوقه")

    #إجراء إعدادي مرحلي
    expert=fields.Boolean(string="تعيين خبير")
    expert_name=fields.Char(string="اسم الخبير")
    expert_address=fields.Char(string="عنوان الخبير")
    expert_number=fields.Char(string="رقم الخبير")

    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)
    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    expert_fee=fields.Monetary(string="أتعاب الخبير", currency_field='company_currency_id')
    expert_result=fields.Char(string="نتيجة الخبرة")
    
    #التأجيل
    postponement=fields.Date(string="يؤجل الى")
    postponement_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_postponement_hijri",readonly=True)




    case_id=fields.Many2one('cases.data',string='رقم الدعوى')

    another_decision_id=fields.Many2one('sessions.data',string='رقم الجلسة')

    expert_installment_ids=fields.One2many('expert.installment','expert_installment_id',string='الدفعات')


    # def name_get(self):
    #     res=[]
    #     for rec in self:
    #         res.append((rec.id,'%s' % (rec.another_decision)))
    #     return res 

    @api.onchange('date')
    def _compute_date_hijri(self):
        for rec in self:
            if rec.date:
                rec.date_hijri = Gregorian.fromdate(rec.date).to_hijri()
            else:
                rec.date_hijri = Hijri.today()
    
    @api.onchange('decision_date')
    def _compute_decision_date_hijri(self):
        for rec in self:
            if rec.decision_date:
                rec.decision_date_hijri = Gregorian.fromdate(rec.decision_date).to_hijri()
            else:
                rec.decision_date_hijri = Hijri.today()
    
    @api.onchange('last_date_for_resumption')
    def _compute_last_date_for_resumption_hijri(self):
        for rec in self:
            if rec.last_date_for_resumption:
                rec.last_date_for_resumption_hijri = Gregorian.fromdate(rec.last_date_for_resumption).to_hijri()
            else:
                rec.last_date_for_resumption_hijri = Hijri.today()
    
    @api.onchange('registration_date')
    def _compute_registration_date_hijri(self):
        for rec in self:
            if rec.registration_date:
                rec.registration_date_hijri = Gregorian.fromdate(rec.registration_date).to_hijri()
            else:
                rec.registration_date_hijri = Hijri.today()
    
    @api.onchange('resupmtion_verdict_date')
    def _compute_resupmtion_verdict_date_hijri(self):
        for rec in self:
            if rec.resupmtion_verdict_date:
                rec.resupmtion_verdict_date_hijri = Gregorian.fromdate(rec.resupmtion_verdict_date).to_hijri()
            else:
                rec.resupmtion_verdict_date_hijri = Hijri.today()
    
    @api.onchange('postponement')
    def _compute_postponement_hijri(self):
        for rec in self:
            if rec.postponement:
                rec.postponement_hijri = Gregorian.fromdate(rec.postponement).to_hijri()
            else:
                rec.postponement_hijri = Hijri.today()

    def action_decision(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'عرض القرار',
            'view_mode': 'form',
            'res_model': 'another.decision',
            'res_id': self.id,
            # 'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False}"
        }