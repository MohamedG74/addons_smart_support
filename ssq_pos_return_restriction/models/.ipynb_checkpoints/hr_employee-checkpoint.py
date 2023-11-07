from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    target_period = fields.Selection([
        ('monthly', 'شهرى'),
        ('quarter', 'ربع سنوى'),
        ('year', 'سنوى')
        ])
    target = fields.Float(string="القيمة المستهدف فوترتها")
    acheived = fields.Float(compute="_compute_total", readonly=True)
    
    @api.depends("target_period")
    def _compute_total(self):        
        for record in self:
            record.acheived = 0
            sale_orders = self.env['sale.order'].search([('user_id', '=', self.user_id.id), ('state', '=', 'sale')])
            for order in sale_orders:
                record.acheived = record.acheived + order.amount_total