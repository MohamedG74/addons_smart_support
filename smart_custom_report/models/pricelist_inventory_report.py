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


class DynamicPricelistInventoryReport(models.Model):

    _name = 'dynamic.pricelist.inventory.report'
    
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
        report_values = self.env['dynamic.pricelist.inventory.report'].search([('id', '=', option[0])])
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
        # print(product_output)

        main_group = '''
            SELECT
                id,name->>'en_US' as name ,x_studio_name_in_ar as namear
            FROM
                pos_category
        '''
        group = self._cr.execute(main_group)
        main_group_output = self._cr.dictfetchall() 

        
        return {
            'name': 'Pricelist Inventory Report',
            'type': 'ir.actions.client',
            'tag': 'pl_i_r',
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
        r = self.env['dynamic.pricelist.inventory.report'].search([('id', '=',option[0])])
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
                WHERE product_product.id = '{0}'
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

                WITH StockSummary AS (
                -- Calculate Opening Stock
                SELECT
                    product_id,
                    SUM(qty_done) AS opening_stock
                FROM
                    stock_move_line
                WHERE
                    reference = 'Product Quantity Updated'
                    AND location_id = 14
                    AND location_dest_id = '{3}'
                    AND date <= '{0}'
                    GROUP BY
                        product_id, date
                    ORDER BY date DESC
                    LIMIT 1
                ),
                
                TotalIn AS (
                    -- Calculate Total In
                    SELECT
                        product_id,
                        COALESCE(SUM(CASE WHEN (location_dest_id != 14 AND location_dest_id = '{3}') THEN qty_done ELSE 0 END), 0) AS total_in
                    FROM
                        stock_move_line
                    WHERE
                        (location_dest_id != 14 AND location_dest_id = '{3}')
                        AND date >= '{0}' AND date <= '{1}'
                    GROUP BY
                        product_id
                ),
                TotalOut AS (
                    -- Calculate Total Out
                    SELECT
                        product_id,
                        COALESCE(SUM(CASE WHEN (location_dest_id != 14 AND location_id = '{3}') THEN qty_done ELSE 0 END), 0) AS total_out
                    FROM
                        stock_move_line
                    WHERE
                        (location_id != 14 AND location_id = '{3}')
                        AND date >= '{0}' AND date <= '{1}'
                    GROUP BY
                        product_id
                ),
                UsageSummary AS (
                    -- Additional Usages
                    SELECT
                        product_id,
                        SUM(CASE
                            WHEN sm.location_dest_id = '{3}' AND sl.usage = 'customer' THEN qty_done
                            ELSE 0
                        END) AS return_from_customer,
                        SUM(CASE
                            WHEN sm.location_id = '{3}' AND sl_dest.usage = 'customer' THEN qty_done
                            ELSE 0
                        END) AS sales_to_customer,
                        SUM(CASE
                            WHEN sm.location_id = '{3}' AND sl_dest.usage = 'supplier' THEN -qty_done
                            ELSE 0
                        END) AS return_from_supplier,
                        SUM(CASE
                            WHEN sm.location_dest_id = '{3}' AND sl.usage = 'supplier' THEN qty_done
                            ELSE 0
                        END) AS purchase_from_supplier,
                        SUM(CASE
                            WHEN sm.location_id = '{3}' AND sl_dest.usage = 'internal' THEN qty_done
                            ELSE 0
                        END) AS transfer_outgoing_location,
                        SUM(CASE
                            WHEN sm.location_dest_id = '{3}' AND sl.usage = 'internal' THEN qty_done
                            ELSE 0
                        END) AS transfer_incoming_location
                    FROM
                        stock_move_line AS sm
                        INNER JOIN stock_location AS sl
                        ON sm.location_id = sl.id
                        LEFT JOIN stock_location AS sl_dest
                        ON sm.location_dest_id = sl_dest.id
                    WHERE
                        date >= '{0}' AND date <= '{1}'
                    GROUP BY
                        product_id
                )
                SELECT
                    product_product.id AS product_id,


                    product_product.default_code AS product_code,
                    product_template.name->>'en_US' AS product_name,

                    uom_uom.name->>'en_US' AS uom_name,
                    product_template.list_price AS list_price,
                
                    product_template.inherit_standard_price AS inherit_standard_price,

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
                    ) AS operating_unit_name,


                    COALESCE(opening_stock, 0) AS opening_stock,
                    COALESCE(total_in, 0) AS total_in,
                    COALESCE(total_out, 0) AS total_out,
                    COALESCE(return_from_customer, 0) AS return_from_customer,
                    COALESCE(sales_to_customer, 0) AS sales_to_customer,
                    COALESCE(return_from_supplier, 0) AS return_from_supplier,
                    COALESCE(purchase_from_supplier, 0) AS purchase_from_supplier,
                    COALESCE(transfer_outgoing_location, 0) AS transfer_outgoing_location,
                    COALESCE(transfer_incoming_location, 0) AS transfer_incoming_location,
                    COALESCE(
                        COALESCE(opening_stock, 0) +
                        COALESCE(total_in, 0) -
                        COALESCE(total_out, 0),
                        0
                    ) AS current_stock
                FROM
                    product_product
                LEFT JOIN product_template ON product_product.product_tmpl_id = product_template.id

                LEFT JOIN pos_category ON product_template.pos_categ_id = pos_category.id
                LEFT JOIN pos_category AS parent_category ON pos_category.parent_id = parent_category.id
                LEFT JOIN uom_uom ON product_template.uom_id = uom_uom.id

                LEFT JOIN StockSummary ON product_product.id = StockSummary.product_id
                LEFT JOIN TotalIn ON product_product.id = TotalIn.product_id
                LEFT JOIN TotalOut ON product_product.id = TotalOut.product_id
                LEFT JOIN UsageSummary ON product_product.id = UsageSummary.product_id
                {2};



                '''.format(date_from,date_to,filters,report_location)

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





class AddCostField(models.Model):
    _inherit='product.template'


    inherit_standard_price=fields.Float(related="product_variant_id.standard_price",string="Inherit Standard Price",store=True)