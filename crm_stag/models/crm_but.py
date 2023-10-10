from odoo import api,fields,models



class New_but_crm(models.Model):
    _inherit='crm.lead'

    crm_stage_nam=fields.Char(related='stage_id.name',string='stage id')
