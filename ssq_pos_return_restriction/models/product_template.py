from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class ProductTemplate(models.Model):
    _inherit = "product.template"

    gurantee = fields.Integer('Gurantee Years')

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    gurantee_end = fields.Date("Gurantee End Date",compute="_compute_total",readonly=True)

    @api.depends("product_id")
    def _compute_total(self):        
        for record in self:
            record.gurantee_end = ""
            try:
                record.gurantee_end = record.date.replace(year=record.date.year + record.product_id.gurantee)
            except ValueError:
                # 👇️ preseve calendar day (if Feb 29th doesn't exist, set to 28th)
                record.gurantee_end = record.date.replace(year=record.date.year + record.product_id.gurantee, day=28)
