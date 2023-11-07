from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = "crm.team"

    target_period = fields.Selection([
        ('monthly', 'شهرى'),
        ('quarter', 'ربع سنوى'),
        ('year', 'سنوى')
        ])
    commission_percent = fields.Float(string="نسبه العمولة للفريق")
    commission_value = fields.Float(string="اجمالى العمولات خلال الشهر",compute="_compute_total_commisson", readonly=True)
    
    acheived = fields.Float(compute="_compute_total", readonly=True)
    @api.depends("pos_order_amount_total")
    def _compute_total(self):        
        for record in self:
            record.acheived = 0
            sale_orders = self.env['sale.order'].search([('team_id', '=', self.id), ('state', '=', 'sale')])
            for order in sale_orders:
                record.acheived = record.acheived + order.amount_total
    
    @api.depends("commission_percent")        
    def _compute_total_commisson(self):
        for record in self:
            record.commission_value = 0
            if(record.commission_percent > 0):                
                record.commission_value = record.acheived * record.commission_percent / 100