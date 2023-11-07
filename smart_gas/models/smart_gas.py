#
# @Author: 
# @Email:
#


from odoo import api, fields, models
from decimal import *

class SmartGas(models.Model):
    _inherit = ['account.move.line']

    thousandcubic = fields.Float(string = 'الاقدام المكعبة')
    
    def compute_heat(self):
        params = self.env['ir.config_parameter'].sudo()
        heating = params.get_param('saving_value.heating', default=False)                     
        return heating
    
    gasvalue = fields.Float(string='القيمة الحرارية', digits='Payment Terms', default=compute_heat)

    @api.onchange('thousandcubic')
    def _onchange_thousand(self):
            self.quantity = Decimal((self.thousandcubic * self.gasvalue)/1000).quantize(Decimal('.0001'), rounding=ROUND_UP)
            #self.thousandcubic = self.thousandcubic
            #"{:.4f}".format(self.thousandcubic * self.gasvalue)
    
    @api.onchange('gasvalue')
    def _onchange_gasvalue(self):
            self.quantity = Decimal((self.thousandcubic * self.gasvalue)/1000).quantize(Decimal('.0001'), rounding=ROUND_UP)
            #self.gasvalue = self.gasvalue 