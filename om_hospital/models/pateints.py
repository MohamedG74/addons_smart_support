from odoo import api , fields , models
from odoo.exceptions import ValidationError

class HospitalPateint(models.Model):
    _name='hospital.pateint'
    _describtion='Pateint_records'
    _inherit='mail.thread'


    p_name=fields.Char(string="Name",tracking=True)
    gender=fields.Selection([('male','Male'),('female','Female'),('others','Others')],string='Gender',tracking=True)
    is_child=fields.Boolean(string="is_child ?",tracking=True)
    age=fields.Integer(string="Age",tracking=True)
    p_id=fields.Char(string='id',default= lambda self:'New')


    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['p_id']=self.env['ir.sequence'].next_by_code('hospital.pateint')
        return super(HospitalPateint,self).create(vals_list)
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age == 0:
                raise ValidationError("You should Enter age !")

    @api.onchange('age')
    def _on_change_age(self):
        if self.age <= 10:
            self.is_child = True
        else:
            self.is_child = False
