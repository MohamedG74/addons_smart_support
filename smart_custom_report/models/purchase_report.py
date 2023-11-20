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


class DynamicPurchaseReport(models.Model):

    _name = 'dynamic.purchase.report'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')
    # report_type = fields.Selection([('report_by_order',
    #                                'Report By Order'),
    #                                ('report_by_product',
    #                                'Report By Product')],
    #                                default='report_by_order')

    @api.model
    def purchase_report(self, option):
        orders = self.env['purchase.order'].search([])
        report_values = self.env['dynamic.purchase.report'].search([('id', '=', option[0])])
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
                id,name->>'en_US' as name ,x_studio_name_in_ar as namear
            FROM
                pos_category
        '''
        group = self._cr.execute(main_group)
        main_group_output = self._cr.dictfetchall() 

        
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.client',
            'tag': 's_r',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'groups':main_group_output,
            'filters': filters,
            'report_lines': lines,
            }


    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.purchase.report'].search([('id', '=',option[0])])
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
        
        

        if data.get('date_from') and data.get('date_to') and data.get('report_location')!='all':
            if(data.get('report_product')!= 'all'):
                filters = filters + """
                WHERE  pp.id = '{0}'
                """.format(data.get('report_product'))
            
            if(data.get('second_group')!= 'all'):
                filters = filters + """
                WHERE pos_category.x_studio_name_in_ar = '{0}'
                """.format(data.get('second_group'))

            if(data.get('main_group')!= 'all'):
                filters = filters + """
                WHERE parent_category.name->>'en_US' = '{0}'
                """.format(data.get('main_group'))
       
            query = \
                '''
                SELECT 
                    pp.id as product_id,
                    pp.default_code AS product_code,
                    pt.name->>'en_US' AS product_name,
                    COALESCE(x.incoming_from_customers, 0) AS incoming_from_customers,
                    COALESCE(x.outgoing_to_customers, 0) AS outgoing_to_customers,
                    COALESCE(x.incoming_from_vendors, 0) AS incoming_from_vendors,
                    COALESCE(x.outgoing_returned_to_vendors, 0) AS outgoing_returned_to_vendors,
                    COALESCE(x.incoming_internal, 0) AS incoming_internal,
                    COALESCE(x.outgoing_internal, 0) AS outgoing_internal,
                    COALESCE(y.opening_stock, 0) AS opening_stock,
                    uom_uom.name->>'en_US' AS uom_name,
                    pos_category.x_studio_name_in_ar as category_name,
                    parent_category.name->>'en_US' as parent_name,
                    (
                        SELECT sw.name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = {3}
                    ) AS warehouse_name,
                    (
                        SELECT ou.x_studio_arabic_name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = {3}
                    ) AS operating_unit_name
                FROM 
                    (SELECT
                        sm.product_id,
                    SUM(CASE WHEN sm.location_dest_id = {3}  AND sm.location_id = 5 THEN sm.qty_done ELSE 0 END) AS incoming_from_customers,
                    SUM(CASE WHEN sm.location_id = {3} AND sm.location_dest_id = 5 THEN -1 * sm.qty_done ELSE 0 END) AS outgoing_to_customers,
                    SUM(CASE WHEN sm.location_dest_id = {3} AND sm.location_id = 4 THEN sm.qty_done ELSE 0 END) AS incoming_from_vendors,
                    SUM(CASE WHEN sm.location_id = {3} AND sm.location_dest_id = 4 THEN -1 * sm.qty_done ELSE 0 END) AS outgoing_returned_to_vendors,
                    SUM(CASE WHEN sm.location_dest_id = {3} AND sm.location_id NOT IN (5,4) THEN sm.qty_done ELSE 0 END) AS incoming_internal,
                    SUM(CASE WHEN sm.location_id = {3} AND sm.location_dest_id NOT IN (5,4,14) THEN -1 * sm.qty_done ELSE 0 END) AS outgoing_internal
                    FROM
                        stock_move_line sm
                    WHERE
                        sm.date >= '{0}' AND sm.date <= '{1}'
                        AND (sm.location_id = '{3}' OR sm.location_dest_id = '{3}')
                    GROUP BY sm.product_id) x
                LEFT JOIN
                    (SELECT
                        SUM(adjusted_quantity) AS opening_stock,
                        product_id
                    FROM (
                        SELECT
                            CASE
                                WHEN location_id = '{3}' THEN -1 * qty_done
                                WHEN location_dest_id = '{3}' THEN qty_done
                            END AS adjusted_quantity,
                        product_id
                        FROM
                            stock_move_line
                        WHERE
                            date < '{0}'
                            AND (location_id = '{3}' OR location_dest_id = '{3}')
                    ) AS subquery 
                    GROUP BY product_id) y
                ON x.product_id = y.product_id
                RIGHT JOIN
                    product_product pp ON x.product_id = pp.id
                JOIN
                    product_template pt ON pp.product_tmpl_id = pt.id
                JOIN
                    uom_uom ON pt.uom_id = uom_uom.id
                LEFT JOIN
                    pos_category ON pt.pos_categ_id = pos_category.id
                LEFT JOIN
                    pos_category AS parent_category ON pos_category.parent_id = parent_category.id
                    {2};
                '''.format(date_from,date_to,filters,report_location)

        if(query != ""):
            print(query)
            self._cr.execute(query)
            report_by_order = self._cr.dictfetchall()
            report_sub_lines.append(report_by_order)
        
        return report_sub_lines


    def _get_report_values(self, data):
        docs = data['model']
        date_from = data.get('date_from')
        date_to = data.get('date_to')

    
     
        # if data['report_type'] == 'report_by_order_detail':
        #     report = ['Report By Order Detail']
        # elif data['report_type'] == 'report_by_product':
        #     report = ['Report By Product']
        # elif data['report_type'] == 'report_by_categories':
        #     report = ['Report By Categories']
        # elif data['report_type'] == 'report_by_purchase_representative':
        #     report = ['Report By Purchase Representative']
        # elif data['report_type'] == 'report_by_state':
        #     report = ['Report By State']
        # else:
        #     report = ['Report By Order']
        # if data.get('report_type'):
        report_res = self._get_report_sub_lines(data,date_from, date_to)
        if len(report_res) > 0:
            report_res = report_res[0]

        # else:
        #     report_res = self._get_report_sub_lines(data, date_from, date_to)
        
        return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}
