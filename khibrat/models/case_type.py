from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Case(models.Model):
    _name = "case.type"
    _rec_name= 'case_type'
    
    # case_category = fields.Selection([('تجارى','تجارى'),
    #                                    ('إدارى','إدارى'),
    #                                    ('عامة','عامة'),
    #                                    ('أحوال','أحوال'),
    #                                    ('عمالية','عمالية'),],string="نوع القضية")
    case_type = fields.Char(string="نوع القضية")

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.case_type)))
        return res
    

    @api.model_create_multi
    def create(self,value):
        for rec in value:
            user = str(rec.get('case_type')).strip()
            if not rec.get('case_type'):
                raise ValidationError(_("برجاء إدخال نوع القضية"))

            self.env.cr.execute("SELECT * FROM case_type WHERE trim(case_type) = %s ",(user,))
            exists = self.env.cr.fetchone()

            if exists:
                raise ValidationError(_("نوع القضية متكرر"))
            else:
                return super(Case, self).create(value)
       