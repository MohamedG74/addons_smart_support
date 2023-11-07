from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Appellate_Judgment_Second(models.Model):
    _name = "appellate.judgmentsecond"
    _rec_name= 'stage_in_appellate_judgment_2'
    
    appellate_judgment_date_2 = fields.Date(string="تاريخه")
    appellate_judgment_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_appellate_judgment_date_2_hijri",readonly=True)

    received_date_2 = fields.Date(string="تاريخ استلامه")
    received_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_received_date_2_hijri",readonly=True)

    appellate_judgment_last_date_for_resumption_2 = fields.Date(string="تاريخ اخر موعد لإستئنافه")
    appellate_judgment_last_date_for_resumption_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_appellate_judgment_last_date_for_resumption_2_hijri",readonly=True)

    appellate_judgment_spoken_2=fields.Selection([('confirmation','تأييد'),('repeal','نقض')],string="منطوقه", required=True)

    appellate_judgment_attach_name_2=fields.Char(string="اسم المستند")
    appellate_judgment_attach_file_2= fields.Binary(string="إرفاق مستند")

    demands_2=fields.Selection([('financial', 'مالى'),('not_financial','غير مالى'),('else','أخرى')],string="الطلبات")
    
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    claiming_2=fields.Monetary(string="اصل الاستحقاق", currency_field='company_currency_id')

    expert_fees_2=fields.Monetary(string="أتعاب الخبره", currency_field='company_currency_id')

    compensation_2=fields.Monetary(string="التعويض", currency_field='company_currency_id')
    
    lawyer_fees_2=fields.Monetary(string="أتعاب المحاماه", currency_field='company_currency_id')

    total_2=fields.Monetary(string="إجمالى المبلغ المحكوم به", currency_field='company_currency_id')
    
    notes_2 = fields.Text(string="طلبات أخرى")
    not_financial_notes_2 = fields.Text(string="طلبات غير مالى")


    @api.onchange('appellate_judgment_date_2')
    def _compute_appellate_judgment_date_2_hijri(self):
        for rec in self:
            if rec.appellate_judgment_date_2:
                rec.appellate_judgment_date_2_hijri = Gregorian.fromdate(rec.appellate_judgment_date_2).to_hijri()
            else:
                rec.appellate_judgment_date_2_hijri = Hijri.today()
    
    @api.onchange('received_date_2')
    def _compute_received_date_2_hijri(self):
        for rec in self:
            if rec.received_date_2:
                rec.received_date_2_hijri = Gregorian.fromdate(rec.received_date_2).to_hijri()
            else:
                rec.received_date_2_hijri = Hijri.today()
    
    @api.onchange('appellate_judgment_last_date_for_resumption_2')
    def _compute_appellate_judgment_last_date_for_resumption_2_hijri(self):
        for rec in self:
            if rec.appellate_judgment_last_date_for_resumption_2:
                rec.appellate_judgment_last_date_for_resumption_2_hijri = Gregorian.fromdate(rec.appellate_judgment_last_date_for_resumption_2).to_hijri()
            else:
                rec.appellate_judgment_last_date_for_resumption_2_hijri = Hijri.today()

    @api.onchange('claiming_2','expert_fees_2', 'compensation_2', 'lawyer_fees_2')
    def onchange_field(self):
        if self.claiming_2 or self.expert_fees_2 or self.compensation_2 or self.lawyer_fees_2:
            self.total_2 = self.claiming_2 + self.expert_fees_2 + self.compensation_2 + self.lawyer_fees_2 



    appellate_judgment_id_2=fields.Many2one('cases.data',string='رقم الدعوى')
    appellate_judgment_stage_id_2 = fields.Selection(related = 'appellate_judgment_id_2.stage', readonly = False)

    appellate_judgment_type_2=fields.Selection([('إدارى', 'إدارى'),('تجارى','تجارى'),
                                    ('أحوال شخصية','أحوال شخصية'),('عمالى','عمالى'),('جنائى','جنائى')],string="نوع الحكم")




    stage_in_appellate_judgment_2=fields.Char(string='المرحلة')

    def action_appellate_judgment_second(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الحكم الاستئنافى الثاني',
            'view_mode': 'form',
            'res_model': 'appellate.judgmentsecond',
            'res_id': self.id,
            'context': "{'create': False}"
        }   