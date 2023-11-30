from odoo import models, fields, api
from datetime import datetime

class ProductReportWizard(models.TransientModel):
    _name = 'product.report.wizard'
    _description = 'Product Report Wizard'

    date_from = fields.Date(string='Date From', required=True)
    date_to = fields.Date(string='Date To', required=True)
    months_order = fields.Integer(string='Months Order', required=True)

    def _get_internal_locations(self):
        return self.env['stock.location'].search([('usage', '=', 'internal'), ('active', '=', True)])

    def _get_current_stock(self, product_id, location_id):
        self.env.cr.execute("""
            SELECT SUM(quantity)
            FROM stock_quant
            WHERE location_id = %s AND product_id = %s
        """, (location_id, product_id))
        res = self.env.cr.fetchone()
        return res[0] if res else 0

    def _get_age_of_first_entry(self, product_id):
        self.env.cr.execute("""
            SELECT (current_date - date) as age_days
            FROM stock_move_line
            WHERE product_id = %s
            ORDER BY date ASC
            LIMIT 1
        """, (product_id,))
        res = self.env.cr.fetchone()
        return res[0] if res else 0


    def _calculate_sales_for_period_by_location(self, product_id, date_from, date_to, operating_unit_id):
        self.env.cr.execute("""
            SELECT SUM(account_move_line.price_subtotal)
            FROM account_move_line
            JOIN account_move ON account_move_line.move_id = account_move.id
            WHERE account_move_line.date >= %s
            AND account_move_line.date <= %s
            AND account_move_line.product_id = %s
            AND account_move.move_type = 'out_invoice'
            AND account_move_line.price_subtotal > 0
            AND account_move.x_studio_branch = %s
        """, (date_from, date_to, product_id, operating_unit_id))
        res = self.env.cr.fetchone()
        return res[0] if res else 0

    def generate_report(self):
        Product = self.env['product.product']
        products = Product.search([])  # Fetch all products
        locations = self._get_internal_locations()  # Fetch all internal locations
        report_lines = []

        for product in products:
            age_days = self._get_age_of_first_entry(product.id)
            product_info = {
                'product_id': product.id,
                'product_name': product.name,
                'age':age_days,
                'locations_data': []
            }

            for location in locations:
                stock_on_hand = self._get_current_stock(product.id, location.id)
                sales_for_period = self._calculate_sales_for_period_by_location(product.id, self.date_from, self.date_to, location.operating_unit_id)
                suggested_order = (sales_for_period or 0) - stock_on_hand  
                product_info['locations_data'].append({
                    'location_id': location.id,
                    'location_name': location.complete_name,
                    'stock_on_hand': stock_on_hand,
                    'sales_for_period': sales_for_period,
                    'suggested_order': suggested_order,
                })


            report_lines.append(product_info)

        # The report_lines list now contains all the data needed for the report, by location.
        # You can return this data to the front-end to display it, or use it to generate a PDF or Excel file.
        return report_lines

    # Include additional logic as required for report presentation and file generation.
