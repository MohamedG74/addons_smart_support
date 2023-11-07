        # Copyright 2017-2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from .num2wordss import num2words

class AccountMove(models.Model):
    _inherit = "account.move"

    amount_total_arabic = fields.Text(
        string="Amount Words",
        compute="_compute_total_words",
    )
    
    @api.depends("amount_total")
    def _compute_total_words(self):
        for rec in self:
            rec.amount_total_arabic = " "
            if rec.amount_total > 0:
                rec.amount_total_arabic = num2words(rec.amount_total, to='currency', lang='ar' , currency="SAR",prefix="فقط", suffix="لاغير" )

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_total_arabic = fields.Text(
        string="Amount Words",
        compute="_compute_total_words",
    )
    
    @api.depends("amount_total")
    def _compute_total_words(self):
        for rec in self:
            rec.amount_total_arabic = " "
            if rec.amount_total > 0:
                rec.amount_total_arabic = num2words(rec.amount_total, to='currency', lang='ar' , currency="SAR",prefix="فقط", suffix="لاغير" )