from odoo import api, fields, models, _

class Demands(models.Model):
    _name = "demands.data"
    _rec_name= 'stage_in_demands'
    
    demands=fields.Selection([('financial', 'مالى'),('not_financial','غير مالى'),('else','أخرى')],string="الطلبات")
    notes = fields.Text(string="طلبات أخرى")
    not_financial_notes = fields.Text(string="طلبات غير مالى")

    
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company)

    company_currency_id = fields.Many2one(
        comodel_name='res.currency',
        string="Company Currency",
        related='company_id.currency_id',
        help="Utility field to express amount currency")

    defendants_rights=fields.Monetary(string="اصل الحق المدعى عليه", currency_field='company_currency_id')

    compensation=fields.Monetary(string="التعويض", currency_field='company_currency_id')

    fees=fields.Monetary(string="أتعاب المحاماه", currency_field='company_currency_id')

    total=fields.Monetary(string="إجمالى المبلغ المطلوب", currency_field='company_currency_id')
    
    stage_in_demands=fields.Char(string='المرحلة')

    demands_id=fields.Many2one('cases.data',string='رقم الدعوى')


    @api.onchange('defendants_rights', 'compensation', 'fees')
    def onchange_field(self):
        if self.defendants_rights or self.compensation or self.fees:
            self.total = self.defendants_rights + self.compensation + self.fees 




    def action_demands(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الطلبات',
            'view_mode': 'form',
            'res_model': 'demands.data',
            'res_id': self.id,
            'context': "{'create': False}"
        }   