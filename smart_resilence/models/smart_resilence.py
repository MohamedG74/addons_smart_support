#
# @Author: 
# @Email:
#


from odoo import api, fields, models
from decimal import *

class SmartResilence(models.Model):
    _inherit = ['project.milestone']
    quantity_numbers = fields.Float(string = 'Number Finished')
    quantity_remaining = fields.Float(string = 'Remaining',compute="_compute_remaining")

    @api.onchange('quantity_numbers')
    def _onchange_thousand(self):
        self.quantity_percentage = 0
        if self.sale_line_id:
          if self.quantity_numbers and self.sale_line_id.product_uom_qty:
                self.quantity_percentage = (self.quantity_numbers / self.sale_line_id.product_uom_qty) 
                
    @api.depends('quantity_numbers')
    def _compute_remaining(self):
      for record in self:
        record.quantity_remaining = 0
        if record.sale_line_id:
          if record.quantity_numbers and record.sale_line_id.product_uom_qty:
                record.quantity_remaining = record.sale_line_id.product_uom_qty - record.quantity_numbers

class SmartResilenceProject(models.Model):
    _inherit = ['project.task']

    def name_get(self):
        name_mapping = dict(super().name_get())
        for task in self:
          name_mapping[task.id] = task.name
        return list(name_mapping.items())
