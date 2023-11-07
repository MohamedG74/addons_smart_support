# -*- coding: UTF-8 -*-

from odoo import models, fields

class ShStockQuant(models.Model):
    _inherit = 'stock.move.line'
    prod_code = fields.Char(related='product_id.default_code',string='Product Code')