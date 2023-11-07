from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Final_Judgment_Second(models.Model):
    _name = "final.judgmentsecond"
    _rec_name= 'stage_in_final_judgment_2'
    
    final_judgment_date_2 = fields.Date(string="تاريخه")
    final_judgment_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_final_judgment_date_2_hijri",readonly=True)

    final_judgment_received_date_2 = fields.Date(string="تاريخ استلامه")
    final_judgment_received_date_2_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_final_judgment_received_date_2_hijri",readonly=True)

    final_judgment_spoken_2=fields.Selection([('confirmation','تأييد'),('repeal','نقض')],string="منطوقه", required=True)

    final_judgment_attach_name_2=fields.Char(string="اسم المستند")
    final_judgment_attach_file_2= fields.Binary(string="إرفاق مستند")
    
    final_judgment_id_2=fields.Many2one('cases.data',string='رقم الدعوى')
    
    final_judgment_stage_id_2 = fields.Selection([('دراسة القضية','دراسة القضية'),
                            ('المرحلة الإبتدائية','المرحلة الإبتدائية'),
                            ('المرحلة الإستئنافية الاولى','المرحلة الإستئنافية الاولى'),
                            ('مرحلة التنفيذ','مرحلة التنفيذ'),
                            ('المرحلة العليا الاولى','المرحلة العليا الاولى'),
                            ('المرحلة الإستئنافية الثانية','المرحلة الإستئنافية الثانية'), 
                            ('المرحلة العليا الثانية','المرحلة العليا الثانية'),
                            ('مرحلة الانتهاء','مرحلة الانتهاء'),],readonly = False)


    stage_in_final_judgment_2=fields.Selection([('دراسة القضية','دراسة القضية'),
                            ('المرحلة الإبتدائية','المرحلة الإبتدائية'),
                            ('المرحلة الإستئنافية الاولى','المرحلة الإستئنافية الاولى'),
                            ('مرحلة التنفيذ','مرحلة التنفيذ'),
                            ('المرحلة العليا الاولى','المرحلة العليا الاولى'),
                            ('المرحلة الإستئنافية الثانية','المرحلة الإستئنافية الثانية'), 
                            ('المرحلة العليا الثانية','المرحلة العليا الثانية'),
                            ('مرحلة الانتهاء','مرحلة الانتهاء'),], default='دراسة القضية',
                            string="المرحلة")

    @api.onchange('final_judgment_date_2')
    def _compute_final_judgment_date_2_hijri(self):
        for rec in self:
            if rec.final_judgment_date_2:
                rec.final_judgment_date_2_hijri = Gregorian.fromdate(rec.final_judgment_date_2).to_hijri()
            else:
                rec.final_judgment_date_2_hijri = Hijri.today()
    
    @api.onchange('final_judgment_received_date_2')
    def _compute_final_judgment_received_date_2_hijri(self):
        for rec in self:
            if rec.final_judgment_received_date_2:
                rec.final_judgment_received_date_2_hijri = Gregorian.fromdate(rec.final_judgment_received_date_2).to_hijri()
            else:
                rec.final_judgment_received_date_2_hijri = Hijri.today()


    def action_final_judgment_second(self):
        for rec in self:
            new_stage = rec.final_judgment_id_2.stage
            rec.write({'stage_in_final_judgment_2':new_stage,
                       'final_judgment_stage_id_2':new_stage})
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'الحكم النهائى',
            'view_mode': 'form',
            'res_model': 'final.judgmentsecond',
            'res_id': self.id,
            'context': "{'create': False}"
        }   