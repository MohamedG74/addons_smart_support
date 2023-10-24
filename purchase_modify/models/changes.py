from odoo import api,models,fields

class ModifyPurchase(models.Model):
    _inherit='purchase.order.line'
    disc_ids=fields.Float(string="Discount %")    
    
    @api.onchange('disc_ids')
    def onchange_price(self):
        for rec in self:
            rec.price_unit=rec.price_unit*(rec.disc_ids/100)
            rec.price_subtotal=rec.product_qty*rec.price_unit*rec.disc_ids
            