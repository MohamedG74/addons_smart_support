from odoo import api, fields, models, _

class Reservation(models.Model):
    _name = "reservation.data"
    
    procedure_x=fields.Selection([('x_1','إلقاء الحجز التحفظى'),
                                  ('x_2','المنع من التصرف'),
                                  ('x_3','المنع من السفر'),
                                  ('x_4','الحراسة القضائية')],string="إجراء إحتياطى")
    

    spoken=fields.Char(string="منطوقه")
    decision_date=fields.Date(string="تاريخ استلام صك القرار")
    last_date_for_resumption=fields.Date(string="تاريخ اخر موعد لإستئنافه")
    resupmtion=fields.Char(string="إستئنافه")

    registration_number=fields.Char(string="رقم القيد")
    registration_date=fields.Date(string="تاريخ القيد")
    resupmtion_circle=fields.Char(string="الدائرة الاستئنافية")
    resupmtion_verdict=fields.Char(string="الحكم الاستئنافى")

    resupmtion_verdict_number=fields.Char(string="رقم الاستئناف")
    resupmtion_verdict_date=fields.Date(string="تاريخ الاستئناف")
    resupmtion_verdict_spoken=fields.Char(string="منطوقه")

    
    reservation_id=fields.Many2one('sessions.data',string='Reservation')
