from odoo import api,fields,models, _


class Maintenancetypes(models.Model):
    _name='maintenance.type'
    _inherit=['mail.thread']
    _describtion='maintenance_types'
    #_inherit='maintenance.request'


    name=fields.Char(string="Name",tracking=True)
    details=fields.Text(string="Details",tracking=True)
    html_code=fields.Html(string="Html",tracking=True)
    upload_file=fields.Binary(string="Upload file",tracking=True)
    document_name = fields.Char(string="File Name",tracking=True)
    loca_=fields.Many2many('main.location',string="Maintenance Location")
