from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Exchange_Notes(models.Model):
    _name = "exchange.notes"
    _rec_name= 'stage_in_exchange_notes'
    
    #تبادل مذكرات
    appointment = fields.Selection([('appointment_1','الموعد الاول'),
                                    ('appointment_2','الموعد الثاني'),
                                    ('appointment_3','الموعد الثالث')],string="الموعد")
    phase = fields.Char(string="الجهة")

    date = fields.Date(string="التاريخ")
    date_hijri = fields.Char(string="التاريخ الهجري", compute="_compute_date_hijri",readonly=True)


    exchange_notes_id=fields.Many2one('cases.data',string='رقم الدعوى')
    stage_in_exchange_notes=fields.Char(string='المرحلة')


    @api.onchange('date')
    def _compute_date_hijri(self):
        for rec in self:
            if rec.date:
                rec.date_hijri = Gregorian.fromdate(rec.date).to_hijri()
            else:
                rec.date_hijri = Hijri.today()

    def action_exchange_notes(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'تبادل مذكرات',
            'view_mode': 'form',
            'res_model': 'exchange.notes',
            'res_id': self.id,
            'context': "{'create': False}"
        }   