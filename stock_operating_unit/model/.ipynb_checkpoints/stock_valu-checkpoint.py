# Copyright 2021 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockValu(models.Model):
    _inherit = "stock.valuation.layer"

    operating_unit_id = fields.Many2one(
        related="stock_move_id.filtering_branch", string="Filtering Branch",store = True
    )