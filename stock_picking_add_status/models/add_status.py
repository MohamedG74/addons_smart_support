from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from decimal import *


class add_button(models.Model):
    _inherit = 'stock.picking'


    counts=fields.Char(string="counts of lines")

    stage=fields.Selection([('x_1','لم يتم الاستلام'),
                            ('x_2','إستلام جزئي'),
                            ('x_3','تم الاستلام')], string="حالة استلام العميل", default='x_1', store=True, readonly=True, compute='_compute_stage')
    
    driver_state=fields.Selection([('x_4','لم يتم الاستلام من السائق'),
                                   ('x_5','تم الاستلام من السائق'),] ,default='x_4', string="حالة استلام السائق")
    
    
    @api.depends('move_ids.actually_received', 'move_ids.quantity_done', 'move_ids.reminder')
    def _compute_stage(self):
        for rec in self:
            if not rec.move_ids:
                rec.stage = 'x_1'
            else:
                moves = rec.move_ids
                total_actually_received = sum(move.actually_received for move in moves)
                total_quantity_done = sum(move.quantity_done for move in moves)

                if total_actually_received == total_quantity_done and total_quantity_done != 0:
                    rec.stage = 'x_3'
                elif total_actually_received == 0:
                    rec.stage = 'x_1'
                elif total_actually_received < total_quantity_done:
                    rec.stage = 'x_2'

                getmove = self.env['account.move'].search([('ref','=',rec.origin)])
                for dd in getmove:
                    #dd._get_delivery()
                    if rec.stage == 'x_1':
                        dd.write({"delivery_status":'no'})
                    elif rec.stage == 'x_2':
                        dd.write({"delivery_status":'part'})
                    elif rec.stage == 'x_3':
                        dd.write({"delivery_status":'done'})


    def action_in_way(self):
        for rec in self:
            rec.driver_state= "x_5"

    def action_add_line(self):
        return {
            # 'name':'Add a line',
            # 'type': 'ir.actions.act_window',
            # 'view_mode': 'form',
            # 'res_model': 'stock.move.line',
            # 'context': {'default_picking_id': self.id},
        }
    

class default_code_stock(models.Model):

    _inherit = 'stock.move'
    default_code = fields.Char(string="Internal Reference",related='product_id.default_code')

    actually_received=fields.Float(string="المستلم فعلياً")
    reminder=fields.Float(string="المتبقي")

    @api.onchange('actually_received')
    def _onchange_actually_received(self):
            self.reminder = Decimal((self.quantity_done - self.actually_received)).quantize(Decimal('.0001'))
    

class stock_picking_kanban(models.Model):

    _inherit = 'stock.picking.type'

    count_none = fields.Integer(compute='_compute_stage_count_none')
    count_partially = fields.Integer(compute='_compute_stage_count_partially')

    def _compute_stage_count_none(self):
        for rec in self:
            rec.count_none = self.env['stock.picking'].search_count([('stage', '=', 'x_1'),('picking_type_id', '=', rec.ids)])

    def _compute_stage_count_partially(self):
        for rec in self:
            rec.count_partially = self.env['stock.picking'].search_count([('stage', '=', 'x_2'),('picking_type_id', '=', rec.ids)])

    
    def get_action_none_stage(self):
        return self._get_action('stock_picking_add_status.action_none_stage')
    
    def get_action_partially_stage(self):
        return self._get_action('stock_picking_add_status.action_partially_stage')