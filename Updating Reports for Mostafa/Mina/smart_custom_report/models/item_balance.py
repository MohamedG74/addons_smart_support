#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api
import io
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicItemBalance(models.Model):

    _name = 'dynamic.item.balance'
    
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
        report_values = self.env['dynamic.item.balance'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        else:
            data.update({'report_location': 'all'})
        
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        else:
            data.update({'report_product': 'all'})
        
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
            'tag': 'i_b',
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
        r = self.env['dynamic.item.balance'].search([('id', '=',option[0])])
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
        report_sub_lines = []
        new_filter = None
        query = ""
        filters=""

        if data.get('report_location') !='all' and data.get('report_product')  == "all":
            if(data.get('second_group')!= 'all'):
                filters = filters + """
                AND pc1.x_studio_name_in_ar = '{0}'
                """.format(data.get('second_group'))

            if(data.get('main_group')!= 'all'):
                filters = filters + """
                AND pc2.name->>'en_US' = '{0}'
                """.format(data.get('main_group'))

            query = \
                '''
                SELECT 
                    pp.id, 
                    pp.default_code, 
                    sq.product_id,
					sq.quantity,
                    pt.name->>'en_US' AS product_name, 
                    uom_uom.name->>'en_US' AS uom_name, 
                    pc2.name->>'en_US' AS parent_category_name, 
                    pc1.x_studio_name_in_ar AS category_name, 
                    COALESCE(sl.current_stock, 0) AS current_stock,
                    (
                        SELECT sw.name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = lioc
                    ) AS warehouse_name,
                    (
                        SELECT ou.x_studio_arabic_name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = lioc 
                    ) AS operating_unit_name
                FROM product_template pt
                JOIN uom_uom ON pt.uom_id = uom_uom.id
                JOIN pos_category pc1 ON pt.pos_categ_id = pc1.id
                LEFT JOIN pos_category pc2 ON pc1.parent_id = pc2.id
                JOIN product_product pp ON pt.id = pp.product_tmpl_id
                LEFT JOIN (
                    SELECT 
                        product_id, 
                        SUM(CASE WHEN location_id = lioc THEN -1 * qty_done ELSE 0 END) +
                        SUM(CASE WHEN location_dest_id = lioc THEN qty_done ELSE 0 END) AS current_stock
                    FROM stock_move_line
                    WHERE location_id = lioc OR location_dest_id = lioc
                    and state = 'done'
                    GROUP BY product_id
                ) sl ON pp.id = sl.product_id
                LEFT JOIN (select sum(quantity) as quantity,product_id from stock_quant where location_id = lioc GROUP BY product_id) sq ON pp.id = sq.product_id
                WHERE pt.pos_categ_id = pc1.id
                {0};
                '''.format(filters).replace('lioc',data.get('report_location'))
            
        
        elif data.get('report_location') !='all' and data.get('report_product') != "all":
            query = \
                '''
                SELECT 
                    pp.id, 
                    pp.default_code, 
                    sq.product_id,
					sq.quantity,
                    pt.name->>'en_US' AS product_name, 
                    uom_uom.name->>'en_US' AS uom_name, 
                    pc2.name->>'en_US' AS parent_category_name, 
                    pc1.x_studio_name_in_ar AS category_name, 
                    COALESCE(sl.current_stock, 0) AS current_stock,

                    
                    (
                        SELECT sw.name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = lioc
                    ) AS warehouse_name,
                    (
                        SELECT ou.x_studio_arabic_name
                        FROM stock_warehouse sw
                        JOIN stock_location sl ON sw.id = sl.warehouse_id
                        JOIN operating_unit ou ON sw.operating_unit_id = ou.id
                        WHERE sl.id = lioc 
                    ) AS operating_unit_name
                FROM product_template pt
                JOIN uom_uom ON pt.uom_id = uom_uom.id
                JOIN pos_category pc1 ON pt.pos_categ_id = pc1.id
                LEFT JOIN pos_category pc2 ON pc1.parent_id = pc2.id
                JOIN product_product pp ON pt.id = pp.product_tmpl_id
                LEFT JOIN (
                    SELECT 
                        product_id, 
                        SUM(CASE WHEN location_id = lioc THEN -1 * qty_done ELSE 0 END) +
                        SUM(CASE WHEN location_dest_id = lioc THEN qty_done ELSE 0 END) AS current_stock
                    FROM stock_move_line
                    WHERE location_id = lioc OR location_dest_id = lioc
                    AND state = 'done'
                    GROUP BY product_id
                ) sl ON pp.id = sl.product_id
                LEFT JOIN (select sum(quantity) as quantity,product_id from stock_quant where location_id = lioc GROUP BY product_id) sq ON pp.id = sq.product_id
                WHERE pt.pos_categ_id = pc1.id and sl.product_id = '{0}';
                '''.format(report_product).replace('lioc',data.get('report_location'))

        if(query != ""):
            # print(query)
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
