from odoo import api,models,fields

class ModifyPurchase(models.Model):
    _inherit='purchase.order.line'
    discount_ids=fields.Float(string="Discount %") 
    discount_amount_ids=fields.Float(string="Discount amount")
   
    
    @api.onchange('discount_ids')
    def _onchange_disc(self):
        for rec in self:
            rec.discount_amount_ids=rec.price_unit*(rec.discount_ids/100)
            rec.price_unit=rec.price_unit-rec.discount_amount_ids
            rec.price_subtotal=rec.product_qty*rec.price_unit
