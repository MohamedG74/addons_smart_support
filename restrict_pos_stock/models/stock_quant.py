# -*- coding: UTF-8 -*-

from odoo import models, fields

class ShStockQuant(models.Model):
    _inherit = 'stock.quant'

    sh_secondary_unit_qty = fields.Float(
        'Secondary On Hand ',
        related="product_id.sh_secondary_uom_onhand"
    )
    sh_secondary_unit = fields.Many2one(
        'uom.uom',
        'Secondary Selling Unit',
        related='product_id.sh_secondary_uom'
    )
