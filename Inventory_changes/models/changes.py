from odoo import api,fields,models

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    app_manage = fields.Char(string='Approval Manager')
    received_by=fields.Many2one('hr.employee',string='Received By')
    waher_house=fields.Many2one('res.users',string='Waherhouse Manager',default=6)
    def action_confirm(self):
        super(StockPicking,self).action_confirm()
        user_name= self.env.user.name
        for i in self:
            i['app_manage']=user_name
        


    