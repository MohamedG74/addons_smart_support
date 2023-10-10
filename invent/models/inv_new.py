from odoo import api,fields,models

class Inv_new(models.Model):
    _inherit='stock.picking'
    approval_id=fields.Many2one('approval.request',string='Approval ID')




    