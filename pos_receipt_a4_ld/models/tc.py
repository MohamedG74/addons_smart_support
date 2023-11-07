# -*- coding: utf-8 -*-
# Part of Lebowski. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models, tools, _
from .num2wordss import num2words

class TccResCurrency(models.Model):
    _inherit = 'res.currency'

    def amount_to_text(self, amount):
        return num2words(amount, to='currency', lang='ar' , currency="KWD",prefix="فقط", suffix="لاغير" )