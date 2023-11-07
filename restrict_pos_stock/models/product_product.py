# -*- coding: UTF-8 -*-

from odoo import models, fields


class ShProductProduct(models.Model):
    _inherit = 'product.product'

    category_id = fields.Many2one(
        "uom.category",
        "UOM Category",
        related="uom_id.category_id"
    )
    second_price = fields.Monetary("Second Unit Price",related="product_tmpl_id.second_price",readonly=False)
    company_notes = fields.Char("Product Notes",related="product_tmpl_id.company_notes")

    def name_get(self):
        #res = super(ShProductProduct, self).name_get(cr, uid, ids, context=context)
        #write the code to here
        #then you can return the product name
        result = []
        for rec in self:
            result.append((rec.id, '%s - %s' % (rec.default_code,rec.name)))
        return result
        #return res
