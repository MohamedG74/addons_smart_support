from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class HotelGuest(models.Model):
    _name = "hotel.guest"
    _inherit = 'mail.thread'
    _description= "guest_records"

    name = fields.Char(string="Name", required=True, tracking=True)
    age = fields.Integer(string="Age", required=True, tracking=True)
    phone_number = fields.Char(string="Phone Number", tracking=True)
    category = fields.Selection([('first class', 'First Class'),('second class','Second Class'),('third class','Third Class')],string="category",tracking=True)
    gender = fields.Selection([('male', 'Male'),('female','Female')],string="Gender")
    is_child= fields.Boolean(string="Is Child?")
    ref = fields.Char(string="Id", default=lambda self: _('New')) #value of New must be default
    room_id=fields.Many2one('hotel.room',string="Room ID")
    @api.onchange('age')   #decorator
    def _onchange_age(x):
        if x.age <= 5:
            x.is_child = True
        else:
            x.is_child = False



    @api.constrains('name','category')
    def _check_name_category_ischild(x):
        for records in x:
            if not records.name:
                raise ValidationError(_("chech your entered data"))


    @api.model_create_multi
    def create(self, value):
        for val in value:
            val['phone_number'] = '1111111111'
            val['ref']= self.env['ir.sequence'].next_by_code('hotel.guest') 
        return super(HotelGuest, self).create(value)

    def button_show(self):
       
        return{
            'name': 'view rooms',
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'hotel.room',
            # 'res_id': self.contracto_id,
            'context': {'create': False}
        }