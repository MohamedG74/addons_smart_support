from odoo import api, fields, models, _


class MaintenTypes(models.Model):

    _inherit = 'maintenance.request'

    types_id = fields.Many2one('maintenance.types', string='Type Name')

    details = fields.Text(related='types_id.details', string='Details', readonly=True)
    write_html = fields.Html(related='types_id.write_html', string='Write HTML', readonly=True)
    document_file = fields.Binary(related='types_id.document_file', string='Document File', readonly=True)
    customer_id = fields.Many2one(related='types_id.customer_id', string='Customer', readonly=True)


class MaintenanceTypes(models.Model):

    _name = "maintenance.types"
    _description = "maintenance"
    _rec_name = "type_name"   # choose wha appear to select in many2one field, override the default

    type_name = fields.Char('Type', required=True)
    details = fields.Text('Details')
    write_html = fields.Html('Write HTML')
    document_file = fields.Binary('Document File', attachment=True)
    customer_id = fields.Many2one('res.partner', string='Customer')






# maintenance.hr_equipment_request_view_form
