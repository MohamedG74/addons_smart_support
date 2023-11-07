# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_partner(self):
        result = super()._loader_params_res_partner()
        result['search_params']['fields'].append('block_days')
        result['search_params']['fields'].append('credit_limit')
        result['search_params']['fields'].append('credit_days')
        result['search_params']['fields'].append('credit_amount')
        return result
