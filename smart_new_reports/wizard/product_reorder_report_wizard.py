from odoo import models, fields, api
from datetime import datetime, timedelta

class ProductReorderReportWizard(models.TransientModel):
    _name = 'product.reorder.report.wizard'
    _description = 'Product Reorder Report Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    minimum_reorder_months = fields.Integer(string='Minimum Reorder Months', required=True)
    reorder_months = fields.Integer(string='Reorder Months', required=True)

    def _get_month_delta(self, date_from, date_to):
        delta = date_to - date_from
        return delta.days / 30  # Roughly estimate months as days/30

    def _calculate_sales(self, product_id, date_from, date_to):
        self.env.cr.execute("""
            SELECT SUM(account_move_line.price_subtotal)
            FROM account_move_line, account_move
            WHERE account_move_line.date >= %s
            AND account_move_line.date <= %s
            AND product_id = %s
            AND account_move.id = account_move_line.move_id
            AND account_move.move_type = 'out_invoice'
            AND account_move_line.price_subtotal > 0
        """, (date_from, date_to, product_id))
        result = self.env.cr.fetchone()
        return result[0] if result else 0

    def _calculate_average_monthly_sales(self, total_sales, date_from, date_to):
        if total_sales is None:  # Check if total_sales is None and return 0 immediately
            return 0
        month_delta = self._get_month_delta(date_from, date_to)
        return total_sales / month_delta if month_delta else 0

    def _calculate_reorder_qty(self, average_monthly_sales, minimum_reorder_months):
        return average_monthly_sales * minimum_reorder_months

    def _get_age_of_first_entry(self, product_id):
        self.env.cr.execute("""
            SELECT (current_date - date) as age_days
            FROM stock_move_line
            WHERE product_id = %s
            ORDER BY date ASC
            LIMIT 1
        """, (product_id,))
        result = self.env.cr.fetchone()
        return result[0] if result else 0

    def _calculate_actual_monthly_sales(self, sales, age_days):
        if sales is None:  # Check if sales is None and return 0 immediately
            return 0
        return (sales / age_days) * 30 if age_days else 0

    def generate_report(self):
        Product = self.env['product.product']
        products = Product.search([])  # Fetch all products
        report_lines = []

        for product in products:
            sales = self._calculate_sales(product.id, self.date_from, self.date_to)
            average_monthly_sales = self._calculate_average_monthly_sales(sales, self.date_from, self.date_to)
            reorder_qty = self._calculate_reorder_qty(average_monthly_sales, self.minimum_reorder_months)
            current_stock = product.qty_available
            forecasted_stock = product.virtual_available
            total_stock = current_stock + forecasted_stock
            age_days = self._get_age_of_first_entry(product.id)
            actual_monthly_sales = self._calculate_actual_monthly_sales(sales, age_days)
            extended_reorder_qty = actual_monthly_sales * self.reorder_months

            suggested_reorder_qty = reorder_qty + extended_reorder_qty - total_stock
            suggested_reorder_qty = max(suggested_reorder_qty, 0)  # Ensure the value is not negative

            report_lines.append({
                'product_id': product.id,
                'product_name': product.name,
                'sales': sales,
                'average_monthly_sales': average_monthly_sales,
                'reorder_qty': reorder_qty,
                'current_stock': current_stock,
                'forecasted_stock': forecasted_stock,
                'total_stock': total_stock,
                'age_days': age_days,
                'actual_monthly_sales': actual_monthly_sales,
                'extended_reorder_qty': extended_reorder_qty,
                'suggested_reorder_qty': suggested_reorder_qty
            })

        # You would then use report_lines to generate your report,
        # whether that's adding to a context to render in QWeb, or to export in Excel.
        return report_lines
