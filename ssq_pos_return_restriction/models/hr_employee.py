from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
import math,calendar
from dateutil.relativedelta import relativedelta  # requires python-dateutil


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
            if record.target_period:
                if record.target_period =='monthly':  
                    start_of_date = datetime(year=datetime.now().year, month=datetime.now().month, day=1)
                    end_of_date = datetime(year=datetime.now().year, month=datetime.now().month, day=calendar.monthrange(datetime.now().year, datetime.now().month)[1])
                
                elif record.target_period == 'quarter':
                    start_of_date = datetime(year=datetime.now().year, month=((math.floor(((datetime.now().month - 1) / 3) + 1) - 1) * 3) + 1, day=1)
                    end_of_date = start_of_date + relativedelta(months=3, seconds=-1)
                
                elif record.target_period == 'year':
                    start_of_date = datetime(year=datetime.now().year, month=1, day=1)
                    end_of_date = datetime(year=datetime.now().year, month=12, day=31)
                # convert end_of_date to datetime object
                sale_orders = self.env['account.move'].search([('x_studio_employee', '=', record.id), ('state', '=', 'posted'), ('date','>=', start_of_date.date()), ('date','<=', end_of_date.date())])
                for order in sale_orders:
                    record.acheived = record.acheived + order.amount_total            