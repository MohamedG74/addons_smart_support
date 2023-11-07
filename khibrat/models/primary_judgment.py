from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Primary_Judgment(models.Model):
    _name = "primary.judgment"
    _rec_name= 'stage_in_primary_judgment'
    
    primary_judgment_date = fields.Date(string="تاريخه")
    primary_judgment_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_primary_judgment_date_hijri",readonly=True)

    received_date = fields.Date(string="تاريخ استلامه")
    received_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_received_date_hijri",readonly=True)
    
    primary_judgment_last_date_for_resumption = fields.Date(string="تاريخ اخر موعد لإستئنافه")
    primary_judgment_last_date_for_resumption_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_primary_judgment_last_date_for_resumption_hijri",readonly=True)

    primary_judgment_spoken=fields.Char(string="منطوقه")

    primary_judgment_attach_name=fields.Char(string="اسم المستند")
    primary_judgment_attach_file= fields.Binary(string="إرفاق مستند")

    demands=fields.Selection([('financial', 'مالى'),('not_financial','غير مالى'),('else','أخرى')],string="الطلبات")
    
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    claiming=fields.Monetary(string="اصل الاستحقاق", currency_field='company_currency_id')

    expert_fees=fields.Monetary(string="أتعاب الخبره", currency_field='company_currency_id')

    compensation=fields.Monetary(string="التعويض", currency_field='company_currency_id')
    
    lawyer_fees=fields.Monetary(string="أتعاب المحاماه", currency_field='company_currency_id')

    total=fields.Monetary(string="إجمالى المبلغ المحكوم به", currency_field='company_currency_id')
    notes = fields.Text(string="طلبات أخرى")
    not_financial_notes = fields.Text(string="طلبات غير مالى")


    @api.onchange('primary_judgment_date')
    def _compute_primary_judgment_date_hijri(self):
        for rec in self:
            if rec.primary_judgment_date:
                rec.primary_judgment_date_hijri = Gregorian.fromdate(rec.primary_judgment_date).to_hijri()
            else:
                rec.primary_judgment_date_hijri = Hijri.today()

    @api.onchange('received_date')
    def _compute_received_date_hijri(self):
        for rec in self:
            if rec.received_date:
                rec.received_date_hijri = Gregorian.fromdate(rec.received_date).to_hijri()
            else:
                rec.received_date_hijri = Hijri.today()

    @api.onchange('primary_judgment_last_date_for_resumption')
    def _compute_primary_judgment_last_date_for_resumption_hijri(self):
        for rec in self:
            if rec.primary_judgment_last_date_for_resumption:
                rec.primary_judgment_last_date_for_resumption_hijri = Gregorian.fromdate(rec.primary_judgment_last_date_for_resumption).to_hijri()
            else:
                rec.primary_judgment_last_date_for_resumption_hijri = Hijri.today()


    @api.onchange('claiming','compensation', 'expert_fees', 'lawyer_fees')
    def onchange_field(self):
        if self.claiming or self.expert_fees or self.compensation or self.lawyer_fees:
            self.total = self.claiming + self.expert_fees + self.compensation + self.lawyer_fees 


    primary_judgment_id=fields.Many2one('cases.data',string='رقم الدعوى')

    primary_judgment_type=fields.Selection([('إدارى', 'إدارى'),('تجارى','تجارى'),
                                    ('أحوال شخصية','أحوال شخصية'),('عمالى','عمالى'),('جنائى','جنائى')],string="نوع الحكم")


    primary_judgment_stage_id = fields.Selection(related = 'primary_judgment_id.stage', readonly = False)

    stage_in_primary_judgment=fields.Char(string='المرحلة')

    def action_primary_judgment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الحكم الابتدائى',
            'view_mode': 'form',
            'res_model': 'primary.judgment',
            'res_id': self.id,
            'context': "{'create': False}"
        }   