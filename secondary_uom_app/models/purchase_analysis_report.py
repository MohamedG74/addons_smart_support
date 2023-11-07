from odoo import api, fields, models, _


class PurchaseReport(models.Model):
	_inherit = "purchase.report"

	secondary_quantity = fields.Float("Secondary Qty",digits=(1,3),default=0.000)


	def _select(self):
		return super(PurchaseReport, self)._select() + ", sum(l.secondary_quantity) as secondary_quantity"


	def _group_by(self):
		return super(PurchaseReport, self)._group_by() + ", l.secondary_quantity"
