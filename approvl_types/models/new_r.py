from odoo import api,fields,models

class Newr(models.Model):
    _inherit='approval.request'
    subj_id=fields.Text(string="Subject")
class New_line(models.Model):
        _inherit='approval.product.line'
        cate_ids_line=fields.Many2one('product.category',string="Category line",related="product_id.categ_id")
        type_ids_line=fields.Selection(string="Type",related="product_id.detailed_type")
