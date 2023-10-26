from odoo import api,models,fields

class ModifyPurchase(models.Model):
    _inherit='account.move.line'
    discount_ids=fields.Float(string="Discount %",store=True) 
    discount_amount=fields.Float(string="Discount amount")

    
    @api.onchange('discount_ids')
    def onchange_fun(self):
        for rec in self:
            rec.discount_amount=rec.price_unit*(rec.discount_ids/100)
            rec.price_unit=rec.price_unit-rec.discount_amount
            rec.price_subtotal=rec.quantity*rec.price_unit

    
    