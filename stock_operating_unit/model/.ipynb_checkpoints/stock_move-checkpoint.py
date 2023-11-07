# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = "stock.move"

    operating_unit_id = fields.Many2one(
        related="location_id.operating_unit_id", string="Source Location Branch"
    )
    operating_unit_dest_id = fields.Many2one(
        related="location_dest_id.operating_unit_id",
        string="Dest. Location Branch",
    )
    filtering_branch = fields.Many2one(
        comodel_name="operating.unit",
        string="Filteration Branch",
        compute="_compute_filter",
        readonly=False,
        store=True
    )
    @api.depends("location_dest_id","location_id")
    def _compute_filter(self):
        for rec in self:
            rec.filtering_branch = False
            if rec.location_id.operating_unit_id:
                rec.filtering_branch = rec.location_id.operating_unit_id
            if rec.location_dest_id.operating_unit_id:
                rec.filtering_branch = rec.location_dest_id.operating_unit_id
        

    @api.constrains("picking_id", "location_id", "location_dest_id")
    def _check_stock_move_operating_unit(self):
        for stock_move in self:
            ou_pick = stock_move.picking_id.operating_unit_id or False
            ou_src = stock_move.operating_unit_id or False
            ou_dest = stock_move.operating_unit_dest_id or False
            if ou_src and ou_pick and (ou_src != ou_pick) and (ou_dest != ou_pick):
                raise UserError(
                    _(
                        "Configuration error. The Stock moves must "
                        "be related to a location (source or destination) "
                        "that belongs to the requesting Branch."
                    )
                )
