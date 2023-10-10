from odoo import api,fields,models


class New_fl(models.Model):
    _name='contract.data'

    contracto_id=fields.Many2one('hr.contract',string="ID")
    contract_nams=fields.Char(string="Name")
    upload_doc=fields.Binary(string='Document')
    doc_name = fields.Char(string="File Name",tracking=True)

    def action_view_info(self):
         return{
            'name': 'view contract',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'contract.data',
            # 'res_id': self.contracto_id,
            'context': {'create': False}
         }