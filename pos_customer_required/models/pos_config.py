# Desarrollado por Ing. Henerson Zambrano <zambranohender@gmail.com>

from odoo.tools.translate import _
from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    require_customer = fields.Selection(
        [
            ("no", "Optional"),
            ("payment", "Required before paying"),
          
        ],
        string="Require Customer",
        default="no",
        help="Require customer for orders in this point of sale:\n"
        "* 'Optional' (customer is optional);\n"
        "* 'Required before paying';\n"
     
    )
