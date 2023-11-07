
from odoo import fields, models, api, tools, _
from odoo.tools import float_is_zero
from odoo.exceptions import UserError
# from itertools import groupby
import logging
_logger = logging.getLogger(__name__)

class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    product_uom_id = fields.Many2one('uom.uom', string='Product UoM', related = "",compute="compute_product_uom")

    @api.onchange('product_uom_id')
    def compute_product_uom(self):
        for res in self:
            res.product_uom_id = False
            if res.uom_id:
                res.product_uom_id = res.uom_id
            
            else:
                res.product_uom_id = False
        

    @api.model
    def _order_line_fields(self, line, session_id=None):
        fields_return = super(PosOrderLine,self)._order_line_fields(line,session_id=None)
       
        if line and line[2] and line[2].get('uom_id'):
            fields_return[2].update({'uom_id':line[2].get('uom_id','')})        
            
        else:
            uom_id = self.get_product_uom(line[2].get('product_id'))
            fields_return[2].update({'uom_id':uom_id})   
        return fields_return
    
    def get_product_uom(self,product_id):
        product = self.env['product.product'].browse(product_id)
        return product.uom_id

class StockPicking(models.Model):
    _inherit='stock.picking'

    def _prepare_stock_move_vals(self, first_line, order_lines):
        rs=super(StockPicking,self)._prepare_stock_move_vals(first_line, order_lines)
        if first_line.product_uom_id:
            rs.update({'product_uom': first_line.product_uom_id.id})
        return rs

    def _create_move_from_pos_order_lines(self, lines):
        self.ensure_one()
        # lines_by_product = groupby(sorted(lines, key=lambda l: l.product_id.id), key=lambda l: l.product_id.id)
        for line in lines:
            order_lines = self.env['pos.order.line'].concat(*line)
            first_line = order_lines[0]
            current_move = self.env['stock.move'].create(
                self._prepare_stock_move_vals(first_line, order_lines)
            )
            if first_line.product_id.tracking != 'none' and (self.picking_type_id.use_existing_lots or self.picking_type_id.use_create_lots):
                for line in order_lines:
                    sum_of_lots = 0
                    for lot in line.pack_lot_ids.filtered(lambda l: l.lot_name):
                        if line.product_id.tracking == 'serial':
                            qty = 1
                        else:
                            qty = abs(line.qty)
                        ml_vals = current_move._prepare_move_line_vals()
                        ml_vals.update({'qty_done':qty})
                        if self.picking_type_id.use_existing_lots:
                            existing_lot = self.env['stock.production.lot'].search([
                                ('company_id', '=', self.company_id.id),
                                ('product_id', '=', line.product_id.id),
                                ('name', '=', lot.lot_name)
                            ])
                            if not existing_lot and self.picking_type_id.use_create_lots:
                                existing_lot = self.env['stock.production.lot'].create({
                                    'company_id': self.company_id.id,
                                    'product_id': line.product_id.id,
                                    'name': lot.lot_name,
                                })
                            ml_vals.update({
                                'lot_id': existing_lot.id,
                            })
                        else:
                            ml_vals.update({
                                'lot_name': lot.lot_name,
                            })
                        self.env['stock.move.line'].create(ml_vals)
                        sum_of_lots += qty
                    if abs(line.qty) != sum_of_lots:
                        difference_qty = abs(line.qty) - sum_of_lots
                        ml_vals = current_move._prepare_move_line_vals()
                        if line.product_id.tracking == 'serial':
                            ml_vals.update({'qty_done': 1})
                            for i in range(int(difference_qty)):
                                self.env['stock.move.line'].create(ml_vals)
                        else:
                            ml_vals.update({'qty_done': difference_qty})
                            self.env['stock.move.line'].create(ml_vals)
            else:
                current_move.quantity_done = abs(sum(order_lines.mapped('qty')))


class Product_uom(models.Model):
    _inherit = "product.product"
    multi_uoms = fields.Boolean("Multi Uom")
    uom_ids = fields.Many2many("uom.uom",string="Available Uom")

class Product_product_uom(models.Model):
    _inherit = "product.template"
    uom_ids = fields.Many2many("uom.uom",string="Select Uom")
    
   
    
     
    
    @api.onchange('uom_ids')
    def _onchange_categ_id(self):
        
        obj = self.env['product.product'].search([])
        for i in obj:
            if i.product_variant_id.id == self.product_variant_id.id:
                i.uom_ids = self.uom_ids
                # i.uom_id = i.uom_ids
                # i.select_uom = self.select_uom
                # o = i.write({
                #     'uom_ids': self.select_uom      
                # })
                # raise UserError(o)

