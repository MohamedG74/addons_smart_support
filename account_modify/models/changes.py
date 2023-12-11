from odoo import api, models, fields


class ModifyAccounting(models.Model):
    _inherit='account.account'


    acc_type=fields.Selection([('رئيسى','رئيسى'),('فرعى','فرعى')],string="Account Type")
    