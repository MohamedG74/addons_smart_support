from odoo import api,fields,models, _
from odoo.exceptions import ValidationError

class Mainrequest(models.Model):
    _inherit='maintenance.request'

    x=fields.Many2one('maintenance.type',string="Test")


    # name_type=fields.Many2many('maintenance.type',string="Name")
    details1=fields.Text(string="Details")
    html_code1=fields.Html(string="Html")
    upload_file1=fields.Binary(string="Upload file")
    document_name1 = fields.Char(string="File Name")
    loca_=fields.Many2many('main.location',string="Maintenance Location")

    @api.onchange('x')
    def onchange_name(self):
        for rec in self:
            if rec.stage_id.name == 'New Request':
                rec.details1=rec.x.details
                rec.html_code1=rec.x.html_code
                rec.upload_file1=rec.x.upload_file
                rec.document_name1=rec.x.document_name


  