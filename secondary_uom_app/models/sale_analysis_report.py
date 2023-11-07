from odoo import api, fields, models, tools, _


class SaleReport(models.Model):
	_inherit = "sale.report"

	secondary_quantity = fields.Float("Secondary Qty",digits=(1,3),default=0.000)


	def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
		fields['secondary_quantity'] = ", l.secondary_quantity as secondary_quantity"
		groupby += ', l.secondary_quantity'
		return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
