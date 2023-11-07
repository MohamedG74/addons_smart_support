from odoo import api, fields, models, _

class Document(models.Model):
    _name = "document.data"
    _rec_name= 'document_name'
    _inherit = 'mail.thread'
    
    document_name=fields.Char(string="اسم المذكرة", tracking=True)
    document_file= fields.Binary(string="المذكرة", tracking=True)
    document_type=fields.Char(string="نوعه", tracking=True)
    document_number=fields.Char(string="رقمه", tracking=True)
    document_value=fields.Char(string="قيمته", tracking=True)
    document_source=fields.Char(string="مصدره", tracking=True)

    document_notes=fields.Text(string="ملاحظات", tracking=True)
    
    document_id=fields.Many2one('cases.data',string=' رقم الدعوى')
    stage_document=fields.Selection(related='document_id.stage')

    document_added_by_user_id_in_document = fields.Integer(string="user id")
    document_added_by_user_name_in_document = fields.Char(string="تم إنشائها بواسطة")
    document_date=fields.Date(string="التاريخ")

    ref = fields.Char(string="رقم المذكرة", default=lambda self: _(' '))

    @api.onchange('document_id')
    def _onchange_id(self):
        for rec in self:
            rec.document_added_by_user_id_in_document=rec.document_id.document_added_by_user_id
            rec.document_added_by_user_name_in_document = rec.document_id.document_added_by_user_name

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.document_name)))
        return res


    @api.model_create_multi
    def create(self,value):
        for val in value:
            val['ref']= self.env['ir.sequence'].next_by_code('document.data') 
        return super(Document, self).create(value)
    

    def action_document(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'المستندات',
            'view_mode': 'form',
            'res_model': 'document.data',
            'res_id': self.id,
            'context': "{'create': False}"
        }   