# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def migrate(cr, installed_version):
    cr.execute(
        "ALTER TABLE stock_quant ADD COLUMN IF NOT EXISTS operating_unit_id int4;"
    )
    