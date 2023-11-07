from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"
    
    after_discount = fields.Monetary("السعر بعد الخصم",compute="_compute_total",readonly=True,store=True)
    amount_discount = fields.Monetary("قيمة الخصم",compute="_compute_totaltwo",readonly=True,store=True)
    is_order_return = fields.Integer(string='Is Refund', related="order_id.refunded_orders_count",readonly=True)

    @api.depends("price_subtotal_incl","order_id")
    def _compute_total(self):  
        #self.ensure_one()
        ordertotal = 0
        disc = 0
        percen = 0
        for record in self:
            
            if record.price_unit < 0:
                disc = disc + abs(record.price_unit)
            else:
                #disc = disc - record.price_subtotal_incl
                ordertotal = ordertotal + abs(record.price_subtotal_incl)
        
        if disc > 0:
            percen = abs(disc) / (abs(ordertotal) + abs(disc)) * 100
            
        for record in self:
            record.after_discount = record.price_subtotal_incl
            try:
                if percen > 0: 
                    record.after_discount = record.price_subtotal_incl - (record.price_subtotal_incl * percen / 100) 
            except ValueError:
                record.after_discount = record.price_subtotal_incl
               
            for record in self:
                if record.is_order_return >= 1:
                    if record.price_subtotal_incl > 0:
                        record.after_discount = 0
                else:                        
                    if record.price_subtotal_incl < 0:
                        record.after_discount = 0


    @api.depends("price_subtotal_incl","after_discount")
    def _compute_totaltwo(self):  
       # self.ensure_one()
        for record in self:
            if record.price_unit > 0:
                record.amount_discount =  record.price_subtotal_incl - record.after_discount
            else:
                record.amount_discount =  0
"""
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"
    
    after_discount = fields.Monetary("السعر بعد الخصم",compute="_compute_total",readonly=True,store=True)
    amount_discount = fields.Monetary("قيمة الخصم",compute="_compute_totaltwo",readonly=True,store=True)
   # is_order_return = fields.Integer(string='Is Refund', related="order_id.refunded_orders_count",readonly=True)

    @api.depends("price_total","move_id")
    def _compute_total(self):  
        #self.ensure_one()
        ordertotal = 0
        disc = 0
        percen = 0
        for record in self:
            
            if record.price_unit < 0:
                disc = disc + abs(record.price_unit)
            else:
                #disc = disc - record.price_subtotal_incl
                ordertotal = ordertotal + abs(record.price_total)
        
        if disc > 0:
            percen = abs(disc) / (abs(ordertotal) + abs(disc)) * 100
            
        for record in self:
            record.after_discount = record.price_total
            try:
                if percen > 0: 
                    record.after_discount = record.price_total - (record.price_total * percen / 100) 
            except ValueError:
                record.after_discount = record.price_total
               
            for record in self:
                if record.is_refund:
                    if record.price_total > 0:
                        record.after_discount = 0
                else:                        
                    if record.price_total < 0:
                        record.after_discount = 0


    @api.depends("price_total","after_discount")
    def _compute_totaltwo(self):  
       # self.ensure_one()
        for record in self:
            if record.price_unit > 0:
                record.amount_discount =  record.price_total - record.after_discount
            else:
                record.amount_discount =  0
"""