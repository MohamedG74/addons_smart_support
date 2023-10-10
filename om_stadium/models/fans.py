from odoo import api, fields, models
from odoo.exceptions import ValidationError

class FanID(models.Model):
    _name = "fan.id"
    _inherit=['mail.thread']
    _description= "fans_info"


    fan_name = fields.Char(string="fan_name", required=True,tracking=True)
    age = fields.Integer(string="Age")
    is_child = fields.Boolean(string="is_child ?",tracking=True)
    gender = fields.Selection([('male', 'Male'),('female','Female'),('others','Others')],string="Gender")
    capital_name=fields.Char(string="capital",compute="_compute_capital_name",store=True)
    ref= fields.Char(string="ref",default=lambda self: 'new')

    @api.model_create_multi
    def create(self,vals_list):
        for vals in vals_list:
            vals['ref']=self.env['ir.sequence'].next_by_code('fan.id')
        return super(FanID,self).create(vals_list)
    @api.depends('fan_name')
    def _compute_capital_name(self):
        for rec in self:
            if rec.fan_name:
                rec.capital_name=rec.fan_name.upper()
            else:
                 rec.capital_name=''
    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if rec.age==0:
                raise ValidationError("You should enter age")
    @api.onchange('age')
    def _on_change_age(self):
        if self.age<=10:
            self.is_child=True
        else:
            self.is_child=False

    
        
    
    

#hospital.patient == hospital_patient


# from odoo import api, fields, models, _, tools
# class AccountAccount(models.Model):
#      _name = "account.account"