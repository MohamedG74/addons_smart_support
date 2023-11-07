from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Final_Judgment(models.Model):
    _name = "final.judgment"
    _rec_name= 'stage_in_final_judgment'
    
    final_judgment_date = fields.Date(string="تاريخه")
    final_judgment_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_final_judgment_date_hijri",readonly=True)

    final_judgment_received_date = fields.Date(string="تاريخ استلامه")
    final_judgment_received_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_final_judgment_received_date_hijri",readonly=True)

    final_judgment_spoken=fields.Selection([('confirmation','تأييد'),('repeal','نقض')],string="منطوقه", required=True)
    final_judgment_attach_name=fields.Char(string="اسم المستند")
    final_judgment_attach_file= fields.Binary(string="إرفاق مستند")
    
    final_judgment_id=fields.Many2one('cases.data',string='رقم الدعوى')
    final_judgment_stage_id = fields.Selection(related = 'final_judgment_id.stage', readonly = False)

    final_judgment_type=fields.Selection([('إدارى', 'إدارى'),('تجارى','تجارى'),
                                    ('أحوال شخصية','أحوال شخصية'),('عمالى','عمالى'),('جنائى','جنائى')],string="نوع الحكم")


    stage_in_final_judgment=fields.Char(string='المرحلة')


    @api.onchange('final_judgment_date')
    def _compute_final_judgment_date_hijri(self):
        for rec in self:
            if rec.final_judgment_date:
                rec.final_judgment_date_hijri = Gregorian.fromdate(rec.final_judgment_date).to_hijri()
            else:
                rec.final_judgment_date_hijri = Hijri.today()
    
    @api.onchange('final_judgment_received_date')
    def _compute_final_judgment_received_date_hijri(self):
        for rec in self:
            if rec.final_judgment_received_date:
                rec.final_judgment_received_date_hijri = Gregorian.fromdate(rec.final_judgment_received_date).to_hijri()
            else:
                rec.final_judgment_received_date_hijri = Hijri.today()


    def action_final_judgment(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'حكم العليا الاولى',
            'view_mode': 'form',
            'res_model': 'final.judgment',
            'res_id': self.id,
            'context': "{'create': False}"
        }   