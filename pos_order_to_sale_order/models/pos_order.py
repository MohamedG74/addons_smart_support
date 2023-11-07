# Copyright (C) 2017 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields,models


class PosOrder(models.Model):
    _inherit = "pos.order"
    operating_unit_id = fields.Many2one('operating.unit', related='config_id.operating_unit_id', string="POS Branch", readonly=True)