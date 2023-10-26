from odoo import api,fields,models

class Newr(models.Model):
    _inherit='approval.request'
    subj_id=fields.Text(string="Subject")
class New_line(models.Model):
        _inherit='approval.product.line'
        cate_ids_line=fields.Many2one('product.category',string="Category line",related="product_id.categ_id")
        type_ids_line=fields.Selection(string="Type",related="product_id.detailed_type")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    app_manage = fields.Char(string='Approval Manager')
    received_by=fields.Many2one('hr.employee',string='Received By')
    waher_house=fields.Many2one('res.users',string='Waherhouse Manager',default=7)
    def action_confirm(self):
        super(StockPicking,self).action_confirm()
        user_name= self.env.user.name
        for i in self:
            i['app_manage']=user_name

        
    # def _get_default_value(self):
    #     return self.env.ref=6



    