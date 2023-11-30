#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
import io

import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter
from dateutil.relativedelta import relativedelta
from datetime import timedelta


class DynamicSuggestedOrderReport(models.Model):

    _name = 'dynamic.re.order'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')
    minimum_reorder_months = fields.Integer(string='Minimum Reorder Months')
    reorder_months = fields.Integer(string='Reorder Months')

    @api.model
    def purchase_report(self, option):
        orders = self.env['purchase.order'].search([])
        report_values = self.env['dynamic.re.order'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        
        if report_values.main_group:
            data.update({'main_group': report_values.main_group})    
        if report_values.second_group:
            data.update({'second_group': report_values.second_group})    
        
        if report_values.minimum_reorder_months:
            data.update({'minimum_reorder_months': report_values.minimum_reorder_months})
        else:
            data.update({'minimum_reorder_months': 1})
        if report_values.reorder_months:
            data.update({'reorder_months': report_values.reorder_months})
        else:
            data.update({'reorder_months': 1})

        filters = self.get_filter(option)
        lines = self._get_report_values(data).get('PURCHASE')
        qr = '''
            SELECT stock_location.id, stock_warehouse.name
            FROM stock_location
            LEFT JOIN stock_warehouse ON stock_location.warehouse_id = stock_warehouse.id
            WHERE stock_location.usage = 'internal' AND stock_location.complete_name LIKE '%/Stock%';
        '''
        locs = self._cr.execute(qr)

        resul = self._cr.dictfetchall()

        product_name = '''
            SELECT
                product_product.id, product_product.default_code, product_template.name->>'en_US' AS name
            FROM
                product_product
            LEFT JOIN product_template ON product_product.product_tmpl_id = product_template.id;
        '''
        prod = self._cr.execute(product_name)
        product_output = self._cr.dictfetchall()

        main_group = '''
            SELECT
                id,name->>'en_US' as name ,x_studio_name_in_ar as namear, parent_id
            FROM
                pos_category
        '''
        group = self._cr.execute(main_group)
        main_group_output = self._cr.dictfetchall() 
        
       
       
        return {
            'name': 'Reorder Report',
            'type': 'ir.actions.client',
            'tag': 'r_o_r',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'groups':main_group_output,
            'filters': filters,
            'report_lines': lines,
            }

   
    def _get_month_delta(self, date_from, date_to):
        delta = relativedelta(date_to, date_from)
        return delta.years * 12 + delta.months
    def _calculate_sales(self, date_from, date_to, product_id):
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
        res = self.env.cr.fetchone()
        if res:
            age_days = res[0].days  # Extract the number of days as a numeric value
            return age_days  # Return the numeric value
        return 0

    def _calculate_actual_monthly_sales(self, sales, age_days):
        if sales is None:  # Check if sales is None and return 0 immediately
            return 0
        return (sales / age_days) * 30 if age_days else 0

    def generate_report(self,date_from,date_to,report_product, main_group, second_group, minimum_reorder_months, reorder_months):
        Product = self.env['product.product']
        filterlist = []
        if report_product != 'all':
            filterlist.append(('id', '=', report_product))

        if main_group != 'all':
            filterlist.append(('pos_categ_id.parent_id.id', '=', main_group))

        if second_group != 'all':
            filterlist.append(('pos_categ_id.id', '=', second_group))
        
        products = Product.search(filterlist)  # Fetch all products

        report_lines = []

        for product in products:
            sales = self._calculate_sales(date_from, date_to, product.id)
            average_monthly_sales = self._calculate_average_monthly_sales(sales, date_from, date_to)
            reorder_qty = self._calculate_reorder_qty(average_monthly_sales, minimum_reorder_months)
            current_stock = product.qty_available
            forecasted_stock = product.virtual_available
            total_stock = current_stock + forecasted_stock
            age_days = self._get_age_of_first_entry(product.id)
            actual_monthly_sales = self._calculate_actual_monthly_sales(sales, age_days)
            rounded_actual_monthly_sales=round(actual_monthly_sales,2)
            extended_reorder_qty = actual_monthly_sales * reorder_months
            rounded_extended_reorder_qty =round(extended_reorder_qty ,2)

            suggested_reorder_qty = reorder_qty + rounded_extended_reorder_qty - total_stock
            suggested_reorder_qty = max(suggested_reorder_qty, 0)  # Ensure the value is not negative

            rounded_suggested_reorder_qty =round(suggested_reorder_qty ,2)

            report_lines.append({
                'parent_name': product.pos_categ_id.parent_id.name,
                'category_name': product.pos_categ_id.name,
                'product_id': product.id,
                'product_code': product.default_code,
                'product_name': product.name,
                'sales': sales,
                'average_monthly_sales': average_monthly_sales,
                'reorder_qty': reorder_qty,
                'current_stock': current_stock,
                'forecasted_stock': forecasted_stock,
                'total_stock': total_stock,
                'age_days': age_days,
                'actual_monthly_sales': rounded_actual_monthly_sales,
                'extended_reorder_qty': rounded_extended_reorder_qty,
                'suggested_reorder_qty': rounded_suggested_reorder_qty
            })

        # You would then use report_lines to generate your report,
        # whether that's adding to a context to render in QWeb, or to export in Excel.
        return report_lines


    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.re.order'].search([('id', '=',option[0])])
        default_filters = {}
        filter_dict = {}
        return filter_dict


    def _get_report_sub_lines(
        self,
        data,
        
        date_from,
        date_to,
        ):
        report_product = data.get('report_product')
        report_location = data.get('report_location')
        report_sub_lines = []
        new_filter = None
        query = ""
        filters=""

        # if data.get('date_from') and data.get('date_to') and data.get('report_location')!='all':
        if data.get('date_from') and data.get('date_to'):
            return [self.generate_report(data.get('date_from'), data.get('date_to'), data.get('report_product'), data.get('main_group'), data.get('second_group'), data.get('minimum_reorder_months'), data.get('reorder_months'))]
        
        return []


    def _get_report_values(self, data):
        docs = data['model']
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        report_res = self._get_report_sub_lines(data,date_from, date_to)
        print(report_res)
        if len(report_res) > 0:
            report_res = report_res[0]
        
        return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}
