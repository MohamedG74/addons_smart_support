from odoo import api,fields,models

class Newr(models.Model):
    _inherit='approval.request'

    test2 = fields.Selection(related="category_id.test1")
    test3=fields.Char(string='Test')

class Newf(models.Model):
    _inherit='approval.category'

    test1=fields.Selection([('required', 'Required'),('optional','Optional'),('no','None')],string='Test')
