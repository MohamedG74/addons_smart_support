from odoo import api, fields, models, _

class Final_Requests(models.Model):
    _name = "final.requests"
    _rec_name= 'stage_in_final_requests'
    
    request_1_client=fields.Char(string="الطلب الاول")
    request_2_client=fields.Char(string="الطلب الثاني")
    request_3_client=fields.Char(string="الطلب الثالث")
    request_4_client=fields.Char(string="الطلب الرابع")
    
    request_1_defendant=fields.Char(string="الطلب الاول")
    request_2_defendant=fields.Char(string="الطلب الثاني")
    request_3_defendant=fields.Char(string="الطلب الثالث")
    request_4_defendant=fields.Char(string="الطلب الرابع")
    
    request_1_interfering=fields.Char(string="الطلب الاول")
    request_2_interfering=fields.Char(string="الطلب الثاني")
    request_3_interfering=fields.Char(string="الطلب الثالث")
    request_4_interfering=fields.Char(string="الطلب الرابع")
    
    request_1_entries=fields.Char(string="الطلب الاول")
    request_2_entries=fields.Char(string="الطلب الثاني")
    request_3_entries=fields.Char(string="الطلب الثالث")
    request_4_entries=fields.Char(string="الطلب الرابع")



    request_from=fields.Selection([('المُدعى','المُدعى'),
                                   ('المُدعى عليه','المُدعى عليه'),
                                   ('الجهة المتدخلة','الجهة المتدخلة'),
                                   ('الجهة المدخلة','الجهة المدخلة'),],string="الطلب من")

    final_request_client_many2many=fields.Many2many('clients.data', string="المُدعى")
    final_request_defendant_many2many=fields.Many2many('defendant.data', string="المُدعى عليه")
    final_request_interfering_many2many=fields.Many2many('interfering.data', string="الجهة المتدخلة")
    final_request_entries_many2many=fields.Many2many('entries.data', string="الجهة المدخلة")



    final_request_clients=fields.One2many('clients.data', 'client_id', related = 'final_requests_id.client_ids', string="المُدعى")
    final_request_many2many_clients=fields.Many2many('clients.data', related = 'final_requests_id.client_many2many_ids', string="المُدعى")
    
    final_request_defendants=fields.One2many('defendant.data','defendant_id', related='final_requests_id.defendant_ids',string="المُدعى عليه")
    final_request_many2many_defendants=fields.Many2many('defendant.data', related='final_requests_id.defendant_many2many_ids',string="المُدعى عليه")

    final_request_interfering_related=fields.One2many('interfering.data','interfering_id', related='final_requests_id.interfering_ids',string="الجهة المتدخلة")
    final_request_many2many_interfering_related=fields.Many2many('interfering.data', related='final_requests_id.interfering_many2many_ids',string="الجهة المتدخلة")
    
    final_request_entries_related=fields.One2many('entries.data','entries_id', related='final_requests_id.entries_ids',string="الجهة المدخلة")
    final_request_many2many_entries_related=fields.Many2many('entries.data',related='final_requests_id.entries_many2many_ids',string="الجهة المدخلة")
    

    final_requests_id=fields.Many2one('cases.data',string='رقم الدعوى')
    stage_in_final_requests=fields.Char(string='المرحلة')


    def action_final_requests(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'الطلبات الختامية',
            'view_mode': 'form',
            'res_model': 'final.requests',
            'res_id': self.id,
            # 'domain': [('driver_id', '=', self.id)],
            'context': "{'create': False}"
        }