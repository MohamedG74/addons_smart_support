# -*- coding: utf-8 -*-

from odoo import models


class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super(PosSessionInherit,
                       self)._loader_params_product_product()
        result['search_params']['fields'].extend(
            ['sh_secondary_uom', 'sh_is_secondary_unit','second_price','gurantee','company_notes','sh_product_discount'])
        return result

    def _loader_params_res_partner(self):
        result = super(PosSessionInherit,
                       self)._loader_params_res_partner()
        result['search_params']['fields'].extend(
            ['commercial_register','company_type'])
        return result
