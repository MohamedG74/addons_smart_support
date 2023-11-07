from odoo import api, fields, models, _

class smart(models.Model):
    
    
    _inherit = 'project.project'

    last_update = fields.Char(string="Last Update", compute= "_compute_last")

    @api.depends('last_update')
    def _compute_last(self):
        for rec in self:
            data = self.env['project.update'].search([('project_id','=',rec.id)], order="id desc", limit=1)
            rec.last_update = data.name