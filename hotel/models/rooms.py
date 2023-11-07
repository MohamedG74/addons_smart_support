from odoo import api,fields,models


class HotelRooms(models.Model):

    _name="hotel.room"
    _description="room_records"


    room_id=fields.Char(string="Room ID",default=lambda self:  'New')
    capacity=fields.Selection([('s','Single'),('d','Double'),('t','Triple')],string="Capacity")
    guest_id=fields.Many2one('hotel.guest',string='Guest ID',required=False)
    reserved=fields.Boolean(string='Reserved')
    r_price=fields.Float(string="Price")
    @api.model_create_multi
    def create(self,value):
        for val in value:
            val['room_id']=self.env['ir.sequence'].next_by_code('hotel.room')  
        return super(HotelRooms,self).create(value)

 