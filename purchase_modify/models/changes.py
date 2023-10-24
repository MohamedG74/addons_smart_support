from odoo import api,models,fields
from odoo.exceptions import ValidationError
class ModifyProduct(models.Model):
    _inherit='product.product'

    brand=fields.Char(string="Brand")
    model_number=fields.Char(string="Model Number")
class ModifyPurchase(models.Model):
    _inherit='purchase.order.line'
    # brand_ids=fields.Char(string='Brand',related='product_id.brand')
    # model_num_ids=fields.Char(string='Model Number',related='product_id.model_number')
    disc_ids=fields.Float(string="Discount %")
    untaxed_ids=fields.Float(string="Untaxed Amount",default='0.0',compute='_compute_untax')
    disc_amount_ids=fields.Float(string="Discount Amount",compute='_compute_disc_amount')
    custom_ids=fields.Float(string="Test",compute='_compute_total')
    # status_ids=fields.Selection([('non urgent','Non Urgent'),('urgent','Urgent'),('semi urgent','Semi Urgent'),('emerg','Emergency')])

    # @api.depends('disc_ids')
    # def _compute_disc(self):
    #     for rec in self:
    #         rec.disc_ids=rec.disc_ids/100


    @api.depends('product_qty','disc_ids','price_unit')
    def _compute_total(self):
        self.disc_ids=self.disc_ids/100
        for rec in self:
           
            rec.custom_ids=rec.product_qty*rec.price_unit*rec.disc_ids
            rec.price_subtotal=rec.price_subtotal-rec.custom_ids

    @api.depends('price_subtotal')
    def _compute_untax(self):
        for rec in self:
            rec.untaxed_ids=rec.price_subtotal
    @api.depends('disc_ids')
    def _compute_disc_amount(self):
        for rec in self:
            rec.disc_amount_ids=rec.price_unit*rec.product_qty*rec.disc_ids