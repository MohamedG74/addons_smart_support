from odoo import api,models,fields
from odoo.exceptions import ValidationError
class ModifyProduct(models.Model):
    _inherit='product.product'

    brand=fields.Char(string="Brand")
    model_number=fields.Char(string="Model Number")


class ModifyPurchase(models.Model):
    _inherit='purchase.order.line'

    brand_ids=fields.Char(string='Brand',related='product_id.brand')
    model_num_ids=fields.Char(string='Model Number',related='product_id.model_number')
    cbm_ids=fields.Float(string="CBM",default='0.0')
    status_ids=fields.Selection([('non urgent','Non Urgent'),('urgent','Urgent'),('semi urgent','Semi Urgent'),('emerg','Emergency')])


    @api.constrains('status_ids')
    def _check_status(self):
        for rec in self:
            if rec.status_ids=='emerg':
                raise ValidationError(str(rec.product_id) +'is Emergency')
