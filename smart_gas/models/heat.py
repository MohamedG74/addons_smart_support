from odoo import api, fields, models, _

class GasValue(models.TransientModel):
    
    _inherit = 'res.config.settings'

    heating = fields.Float(string="القيمة الحرارية")

    @api.model
    def get_values(self):
        res = super(GasValue, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        heating = params.get_param('saving_value.heating', default=False)
        res.update(
            heating=heating
        )
        return res

    def set_values(self):
        super(GasValue, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("saving_value.heating",self.heating)    