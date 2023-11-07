from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PosOrder(models.Model):
    _inherit = "pos.order"
    
    discount_value=fields.Float(string="dis")


    tot_disc = fields.Monetary("الخصم",compute="_compute_total",readonly=True)
    tot_disc_before = fields.Monetary("الاجمالى قبل الخصم",compute="_compute_total_two",readonly=True)
    @api.depends("lines")
    def _compute_total(self): 
        #self.tot_disc = 0
        for record in self:
            record.tot_disc = 0
            for rec in record.lines:
                if abs(rec.amount_discount) > 0:
                    record.tot_disc = record.tot_disc +  abs(rec.amount_discount)
                
                    
    @api.depends("tot_disc","amount_total")
    def _compute_total_two(self):  
        for record in self:
            record.tot_disc_before = 0
            if abs(record.tot_disc) > 0:
                record.tot_disc_before = abs(record.amount_total) + abs(record.tot_disc)
            else:
                record.tot_disc_before = abs(record.amount_total)
            
            
            """
            <field string='الاجمالى قبل الخصم' name="tot_disc_before" />
            """

class AccountInv(models.Model):
    _inherit = "account.move"
    
    tot_disc = fields.Monetary(":الخصم",compute="_compute_total",readonly=True)
    tot_disc_before = fields.Monetary(":الاجمالى قبل الخصم",compute="_compute_total_two",readonly=True)

    stot_disc = fields.Monetary("الخصم",readonly=True)
    stot_disc_before = fields.Monetary("الاجمالى قبل الخصم",readonly=True)
    
    is_imported = fields.Boolean("Imported Invoice",default=False)

    @api.depends("invoice_line_ids")
    def _compute_total(self): 
        for this in self:
            this.tot_disc = 0
            if(this.id and this.move_type != "entry" and this.state != "posted"):
                if(this.is_imported == False):
                    for record in this.invoice_line_ids:
                        if record.product_id.default_code == "DISC":
                            this.tot_disc = this.tot_disc +  abs(record.price_subtotal)
                    if this.stot_disc == 0 or this.stot_disc =="":
                        this.write({'stot_disc':this.tot_disc})
                
                    
    @api.depends("tot_disc","amount_total")
    def _compute_total_two(self):  
        for record in self:
            record.tot_disc_before = 0
            if(record.id and record.move_type != "entry" and record.state != "posted"):
                if(record.is_imported == False):
                    if abs(record.tot_disc) > 0:
                        record.tot_disc_before = abs(record.amount_total) + abs(record.tot_disc)
                    else:
                        record.tot_disc_before = abs(record.amount_total)
                    if record.stot_disc_before == 0 or record.stot_disc_before =="":
                        record.write({'stot_disc_before':record.tot_disc_before})
                
