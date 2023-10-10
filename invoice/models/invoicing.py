from odoo import api, fields, models, _


class InvoiceInvoicing(models.Model):

    _inherit = 'product.template'
    heated_val = fields.Float(string='Heated Value')

#
# class InvoiceAccounting(models.Model):
#     # account.view_move_form
#     _inherit = 'account.move'


