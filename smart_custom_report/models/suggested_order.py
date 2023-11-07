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


class DynamicSuggestedOrderReport(models.Model):

    _name = 'dynamic.suggested.order'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')


    @api.model
    def purchase_report(self, option):
        orders = self.env['purchase.order'].search([])
        report_values = self.env['dynamic.suggested.order'].search([('id', '=', option[0])])
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
        
        intnrl =[]
        for rec in self._get_internal_locations():
            intnrl.append({'complete_name':rec.complete_name})
        
        return {
            'name': 'Suggested Order Report',
            'type': 'ir.actions.client',
            'tag': 's_o_r',
            'orders': data,
            'locations':resul,
            'internal': intnrl,
            'products':product_output,
            'groups':main_group_output,
            'filters': filters,
            'report_lines': lines,
            }
    




    def _get_internal_locations(self):
        return self.env['stock.location'].search([('usage', '=', 'internal'), ('active', '=', True),('operating_unit_id','!=',False)])

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
        if res:
            age_days = res[0].days  # Extract the number of days
            return f"{age_days} يوم"
        return "0 يوم"
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


    def generate_report(self,date_from,date_to,report_product, main_group, second_group):            
        Product = self.env['product.product']
        filterlist = []
        if report_product != 'all':
            filterlist.append(('id', '=', report_product))

        if main_group != 'all':
            filterlist.append(('pos_categ_id.parent_id.id', '=', main_group))

        if second_group != 'all':
            filterlist.append(('pos_categ_id.id', '=', second_group))

        products = Product.search(filterlist)  # Fetch all products
        locations = self._get_internal_locations()  # Fetch all internal locations
        
        report_lines = []


        for product in products:
            age_days = self._get_age_of_first_entry(product.id)
            product_info = {
                'product_id': product.id,
                'product_name': product.name,
                'product_code': product.default_code,
                'uom_name': product.uom_id.name,
                'parent_name': product.pos_categ_id.parent_id.name,
                'category_name': product.pos_categ_id.name,
                'age':age_days,
                'locations_data': []
            }

            for location in locations:
                stock_on_hand = self._get_current_stock(product.id, location.id)
                sales_for_period = self._calculate_sales_for_period_by_location(product.id, date_from, date_to, location.operating_unit_id.id)
                suggested_order = (sales_for_period or 0) - (stock_on_hand or 0)   
                product_info['locations_data'].append({
                    'location_id': location.id,
                    'location_name': location.complete_name,
                    'stock_on_hand': stock_on_hand,
                    'sales_for_period': sales_for_period,
                    'suggested_order': suggested_order,
                })


            report_lines.append(product_info)
            # print(product_info['product_name'])

        # The report_lines list now contains all the data needed for the report, by location.
        # You can return this data to the front-end to display it, or use it to generate a PDF or Excel file.
        return report_lines





    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.suggested.order'].search([('id', '=',option[0])])
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
            return [self.generate_report(data.get('date_from'), data.get('date_to'), data.get('report_product'), data.get('main_group'), data.get('second_group'))]
        
        return []


    def _get_report_values(self, data):
        docs = data['model']
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        report_res = self._get_report_sub_lines(data,date_from, date_to)
        #report_res = self.generate_report()
        # print(report_res)
        
        if len(report_res) > 0:
            report_res = report_res[0]
        
        return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}
