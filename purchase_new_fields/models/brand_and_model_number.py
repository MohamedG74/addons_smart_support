from odoo import api, fields, models, _
from decimal import *

class Brand(models.Model):
    _inherit = 'product.template'

    brand = fields.Char(string="Brand")
    model_number = fields.Char(string="Model Number")


class Brand_Product(models.Model):
    _inherit = 'product.product'

    brand_product = fields.Char(related='product_variant_id.brand', string="Brand", readonly=False)
    model_number_product = fields.Char(related='product_variant_id.model_number', string="Model Number", readonly=False)


class Brand_Purchase(models.Model):
    _inherit = 'purchase.order.line'

    brand_purchase = fields.Char(string="Brand", compute='_compute_brand_purchase')
    model_number_purchase = fields.Char(string="Model Number", compute='_compute_model_number_purchase')
    cbm = fields.Float(string="CBM",optional="hide")
    status = fields.Selection([('non', 'Non-Urgent'),
                             ('semi','Semi-Urgent'),
                             ('urgent','Urgent'),
                             ('very','Very-Urgent'),
                             ('emergency','Emergency')], string="Status")
    
    @api.depends('product_id')
    def _compute_brand_purchase(self):
        for rec in self:
            if rec.product_id.brand_product:
                rec.brand_purchase = rec.product_id.brand_product
            else:
                rec.brand_purchase = 0

    @api.depends('product_id')
    def _compute_model_number_purchase(self):
        for rec in self:
            if rec.product_id.model_number_product:
                rec.model_number_purchase = rec.product_id.model_number_product
            else:
                rec.model_number_purchase = 0