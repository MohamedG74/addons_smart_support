from odoo import api, fields, models, _

class Maintenace(models.Model):
    _name = "maintenance.types"
    _description= "maintenance"
    

    name = fields.Char(string="Name")
    details=fields.Char(string="Details")
    writing = fields.Html(string="Write Html")    


class Locations(models.Model):
    _name = "maintenance.locations"
    _description= "maintenance_locations"    

    location_id = fields.Char(string="ID")
    location_name = fields.Char(string="Name")
    location_code = fields.Many2one('code.data', string="Location Code")
    location_address = fields.Char(string="Address")
    location_type = fields.Char(string="Type")
    location_classification = fields.Selection([('external','External'),
                                                ('internal','Internal'),],string="Classification")

    location_customer=fields.Many2one('res.partner', string="Customer")
    location_equipment=fields.Many2one('maintenance.equipment', string="Equipment")
    location_link=fields.Char(string="Location Link")
    notes = fields.Text(string="Notes")

    def name_get(self):
        res=[]
        for rec in self:
            res.append((rec.id,'%s' % (rec.location_code)))
        return res    


class MaintenaceRequest(models.Model):
    _inherit = 'maintenance.request'
    
    request_id = fields.Many2one('maintenance.types', string="Maintenance Request")
    loctaion_id=fields.Many2one('code.data', string="Maintenance locations")
    details_in_request=fields.Char(string="Details")

    @api.onchange('request_id')
    def _onchange_id(self):
        for rec in self:
            if self.stage_id.name == 'New Request':
                rec.name=rec.request_id.name
                rec.description = rec.request_id.writing
                rec.details_in_request = rec.request_id.details
