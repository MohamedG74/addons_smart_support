from odoo import api,models,fields

class HospitalDoctor(models.Model):
    _name='hospital.doctor'
    _inherit=['mail.thread']

    dr_id=fields.Char(string='ID',default=lambda self: 'new')
    dr_name=fields.Char(string='Name')
    address=fields.Text(string='Address')
    age=fields.Integer(string='Age')
    gender=fields.Selection([('male','Male'),('female','Female'),('others','Others')],string='Gender')

    
    
    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['dr_id']=self.env['ir.sequence'].next_by_code('hospital.doctor')
        return super(HospitalDoctor,self).create(vals_list)