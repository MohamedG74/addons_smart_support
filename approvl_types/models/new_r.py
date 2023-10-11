from odoo import api,fields,models

class Newr(models.Model):
    _inherit='approval.request'

    test2 = fields.Selection(related="category_id.test1")
    test3=fields.Char(string='Test')

class Newf(models.Model):
    _inherit='approval.category'

    test1=fields.Selection([('required', 'Required'),('optional','Optional'),('no','None')],string='Test')


class New_line(models.Model):
        _inherit='approval.product.line'

        cate_ids_line=fields.Many2one('product.category',string="Category line",related="product_id.categ_id")
        type_ids_line=fields.Selection(string="Type",related="product_id.detailed_type")
        # @api.depends('product_id')
        # def _compute_category(self):
        #     for rec in self:
        #         if rec.product_id:
        #             rec.cate_ids_line=rec.product_id.categ_id
        #         else:
        #             rec.cate_ids_line = False
