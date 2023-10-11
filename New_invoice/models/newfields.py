from odoo import api,fields,models


class New_filds(models.Model):

    _inherit='account.move.line'

    categ_id_line=fields.Many2one('product.category',string="Category",related='product_id.categ_id')

