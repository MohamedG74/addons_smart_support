from odoo import fields,models,api

class OrderMethods(models.Model):
    _inherit='pos.order'


    payment_meth=fields.Many2many('pos.payment.method',string="Payment_Method",compute="_compute_payment")
   

    @api.depends('payment_ids.payment_method_id')
    def _compute_payment(self):
        for rec in self:
            if rec.payment_ids.payment_method_id:
                rec.payment_meth = rec.payment_ids.payment_method_id


       
    