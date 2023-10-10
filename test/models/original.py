from odoo import api,fields,models


class exist_hr(models.Model):
    _inherit='hr.contract'

    contracto_ids=fields.One2many('contract.data','contracto_id',string="ID")
