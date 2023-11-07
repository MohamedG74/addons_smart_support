from odoo import api, fields, models
from decimal import *
from odoo.exceptions import UserError,  AccessError, MissingError

class SmartAccount(models.Model):
    _inherit = ['account.move']

    delivery_status = fields.Selection(
        selection=[('no', 'لم يتم الاستلام'), ('part', 'تم الاستلام جزئياً'), ('done', 'تم الاستلام بالكامل')],
        string='حالة الاستلام',compute="_get_delivery",readonly=1,default="no",store=True)

    @api.depends('ref')
    def _get_delivery(self):
         for record in self:

             record.delivery_status = "no"
            #  picking = self.env["stock.picking"].search([("origin","=",record.ref)])
            #  for rec in picking:
            #     if rec.stage == 'x_1':
            #         record.delivery_status = 'no'
            #     elif rec.stage == 'x_2':
            #         record.delivery_status = 'part'
            #     elif rec.stage == 'x_3':
            #         record.delivery_status = 'done'