from odoo import api, fields, models
from decimal import *
from odoo.exceptions import UserError,  AccessError, MissingError

class StockPick(models.Model):
    _inherit = ['stock.move']

    # @api.onchange('actually_received')
    # def changed_quantity(self):        
    #     for move in self:
    #         if(move.origin):
    #             getmove = self.env['account.move'].search([('ref','=',move.origin)])
    #             if(getmove and getmove.id):
    #                 for dd in getmove:
    #                     dd._get_delivery()

class StockPicking(models.Model):
    _inherit = ['stock.picking']

    # @api.onchange('stage')
    # def changed_quantity(self):        
    #     for move in self:
    #         if(move.origin):
    #             getmove = self.env['account.move'].search([('ref','=',move.origin)])
    #             if(getmove and getmove.id):
    #                 for dd in getmove:
    #                     dd._get_delivery()