from odoo import api, fields, models, _
from .hijri_converter.convert import Gregorian, Hijri

class Expert_Installments(models.Model):
    _name = "expert.installment"

#الدفعة الاولي
    installment=fields.Selection([('installment_1','الدفعة الاولي'),
                                  ('installment_2','الدفعة الثانية'),
                                  ('installment_3','الدفعة الثالثة')],string="الدفعات")
    
    opponent=fields.Char(string="الخصم")
    client=fields.Char(string="الموكل")

    pay_date=fields.Date(string="تاريخ تسديدها")
    pay_date_hijri=fields.Char(string="التاريخ الهجرى", compute="_compute_pay_date_hijri",readonly=True)


    expert_installment_id=fields.Many2one('another.decision', string='expert_installment_id')     

    @api.onchange('pay_date')
    def _compute_pay_date_hijri(self):
        for rec in self:
            if rec.pay_date:
                rec.pay_date_hijri = Gregorian.fromdate(rec.pay_date).to_hijri()
            else:
                rec.pay_date_hijri = Hijri.today()