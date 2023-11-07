from odoo import models, fields

class PurchaseOrderProject(models.Model):
    
    _inherit = ['purchase.order']

    project_link_id = fields.Many2one('project.project',string="Project")


class PurchaseOrderLineLink(models.Model):
    
    _inherit = ['purchase.order.line']

    def _compute_analytic_distribution(self):
        super()._compute_analytic_distribution()
        for line in self:
            if line.order_id.project_link_id:
                line.analytic_distribution = {line.env['project.project'].browse(line.order_id.project_link_id.id).analytic_account_id.id: 100}
