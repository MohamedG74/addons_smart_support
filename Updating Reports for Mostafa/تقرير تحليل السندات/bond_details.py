#!/usr/bin/python
# -- coding: utf-8 --

from odoo import models, fields, api
from odoo.exceptions import UserError
import io
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicBondDetails(models.Model):

    _name = 'dynamic.bond.details'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')
    bond_number=fields.Char(string='Bond Number')
    exports_from=fields.Char(string='Exports from')
    imports_to=fields.Char(string='Imports To')
    bond_type=fields.Char(string='Bond Type')
    bond_type_sales=fields.Selection([('all','all'),('incoming','incoming'),
                                    ('outgoing','outgoing'),],string='Bond Sales')
    

    counting=fields.Char(string='counting')
    limited=fields.Integer(string='Limited')

                                    
    # report_type = fields.Selection([('report_by_order',
    #                                'Report By Order'),
    #                                ('report_by_product',
    #                                'Report By Product')],
    #                                default='report_by_order')

    @api.model
    def purchase_report(self, option):
        report_values = self.env['dynamic.bond.details'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        else:
            data.update({'report_product': 'all'})
        
        if report_values.main_group:
            data.update({'main_group': report_values.main_group})    
        if report_values.second_group:
            data.update({'second_group': report_values.second_group})

        if report_values.bond_number:
            data.update({'bond_number': report_values.bond_number})
        else:
            data.update({'bond_number': "all"})
        
        if report_values.exports_from:
            data.update({'exports_from': report_values.exports_from})
        else:
            data.update({'exports_from': "all"})
        
        if report_values.imports_to:
            data.update({'imports_to': report_values.imports_to})
        else:
            data.update({'imports_to': "all"})
        
        if report_values.bond_type:
            data.update({'bond_type': report_values.bond_type})
        else:
            data.update({'bond_type': "all"})
        
        if report_values.bond_type_sales:
            data.update({'bond_type_sales': report_values.bond_type_sales})   
        else:     
            data.update({'bond_type_sales': "all"})   

        

        if report_values.counting:
            data.update({'counting': report_values.counting})
        else:
            data.update({'counting': 0})
        
        if report_values.limited:
            data.update({'limited': report_values.limited})
        else:
            data.update({'limited': 25})


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

        exports_from = '''
            select id,name
            from stock_warehouse 
        '''
        exports = self._cr.execute(exports_from)
        exports_from_imports_to_output = self._cr.dictfetchall()
        
        
        bond_type = '''
            select distinct(name)->>'ar_001' as nameara
            from stock_picking_type 
            where name IS NOT NULL;
        '''
        bond = self._cr.execute(bond_type)
        bond_type_output = self._cr.dictfetchall()

        count = self._get_report_values(data).get('count')
        limited = self._get_report_values(data).get('limited')
        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.client',
            'tag': 'b_d',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'groups':main_group_output,
            'exports':exports_from_imports_to_output,
            'bond':bond_type_output,
            'filters': filters,
            'report_lines': lines,
            'count': count,
            'limited': limited,
            }


    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.bond.details'].search([('id', '=',option[0])])
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

        counting = 0
        limited = 25

        if(data.get('counting')):
            counting = data.get('counting')
        
        if(data.get('limited')):
            limited = data.get('limited')
        

        if data.get('date_from') and data.get('date_to') and data.get('report_product') != "all":
            query = \
                '''
                SELECT subq.file_name,
                    subq.picking_id,
                    subq.product_id,
                    subq.reference,
                    prod.default_code AS product_code,
                    uom.name->>'en_US' AS product_uom_name,
                    subq.qty_done,
                    loc1.name AS location_id_name,
                    loc2.name AS location_dest_id_name,
                    DATE(subq.date),
                    stock_picking.name AS pick_name,
                    stock_picking.origin,
                    stock_picking.picking_type_id,
                    stock_picking_type.name->>'ar_001' AS picking_type_name,
                    stock_picking_type.code,
                    pos_cat1.x_studio_name_in_ar AS pos_category_name,
                    pos_cat2.name->>'en_US' AS pos_category_parent_name,
                       CASE 
						WHEN loc1.id = 4 AND loc2.id <> 4   THEN 'مرتجعات'
						ELSE 'مبيعات'
					END AS code,

                    
                    CASE 
						WHEN loc1.id = 14 THEN 'جرد'
						ELSE wh1.name 
					END AS warehouse_id_name,
                    
                    CASE 
						WHEN  stock_picking_type. = 14 THEN 'جرد'
						ELSE wh1.name 
					END AS warehouse_id_name,
                    
                   
                    CASE 
						WHEN loc2.id = 14 THEN 'عجز المخزون'
						ELSE wh2.name 
					END AS warehouse_dest_id_name
                FROM (
                    SELECT stock_move.name AS file_name,
                        stock_move.picking_id,
                        stock_move.reference,
                        stock_move_line.product_id,
                        stock_move_line.product_uom_id,
                        stock_move_line.qty_done,
                        stock_move_line.location_id,
                        stock_move_line.location_dest_id,
                        stock_move.date
                    FROM stock_move 
                    JOIN stock_move_line ON stock_move.id = stock_move_line.move_id 
                    WHERE stock_move.picking_id IS NOT NULL
                        AND stock_move.date BETWEEN '{0}' AND '{1}'
                ) AS subq
                JOIN stock_picking ON subq.picking_id = stock_picking.id
                JOIN stock_location AS loc1 ON subq.location_id = loc1.id
                JOIN stock_location AS loc2 ON subq.location_dest_id = loc2.id
                JOIN product_product AS prod ON subq.product_id = prod.id
                JOIN uom_uom AS uom ON subq.product_uom_id = uom.id
                JOIN stock_picking_type ON stock_picking.picking_type_id = stock_picking_type.id
                LEFT JOIN product_template AS prod_tmpl ON prod_tmpl.id = prod.product_tmpl_id
                LEFT JOIN pos_category AS pos_cat1 ON pos_cat1.id = prod_tmpl.pos_categ_id
                LEFT JOIN pos_category AS pos_cat2 ON pos_cat1.parent_id = pos_cat2.id
                LEFT JOIN stock_warehouse AS wh1 ON loc1.warehouse_id = wh1.id
                LEFT JOIN stock_warehouse AS wh2 ON loc2.warehouse_id = wh2.id
                WHERE subq.product_id = {2}
                LIMIT {3} OFFSET {4};
                '''.format(date_from,date_to,report_product,limited,counting)


            querycount =  '''
            SELECT COUNT(*) AS total_rows
            FROM 
                (
                    SELECT stock_move.name AS file_name,
                        stock_move.picking_id,
                        stock_move.reference,
                        stock_move_line.product_id,
                        stock_move_line.product_uom_id,
                        stock_move_line.qty_done,
                        stock_move_line.location_id,
                        stock_move_line.location_dest_id,
                        stock_move.date
                    FROM stock_move 
                    JOIN stock_move_line ON stock_move.id = stock_move_line.move_id 
                    WHERE stock_move.picking_id IS NOT NULL
                        AND stock_move.date BETWEEN '{0}' AND '{1}'
                ) AS subq
                JOIN stock_picking ON subq.picking_id = stock_picking.id
                JOIN stock_location AS loc1 ON subq.location_id = loc1.id
                JOIN stock_location AS loc2 ON subq.location_dest_id = loc2.id
                JOIN product_product AS prod ON subq.product_id = prod.id
                JOIN uom_uom AS uom ON subq.product_uom_id = uom.id
                JOIN stock_picking_type ON stock_picking.picking_type_id = stock_picking_type.id
                LEFT JOIN product_template AS prod_tmpl ON prod_tmpl.id = prod.product_tmpl_id
                LEFT JOIN pos_category AS pos_cat1 ON pos_cat1.id = prod_tmpl.pos_categ_id
                LEFT JOIN pos_category AS pos_cat2 ON pos_cat1.parent_id = pos_cat2.id
                LEFT JOIN stock_warehouse AS wh1 ON loc1.warehouse_id = wh1.id
                LEFT JOIN stock_warehouse AS wh2 ON loc2.warehouse_id = wh2.id
            ;
            '''.format(date_from,date_to)
            self._cr.execute(querycount)
            report_number_pages = self._cr.dictfetchall()[0]
            report_sub_lines.append(report_number_pages)   

            
        elif data.get('date_from') and data.get('date_to') and data.get('report_product') == "all":
           
                      
            if(data.get('second_group')!= 'all'):
                filters = filters + """
                AND pos_cat1.x_studio_name_in_ar = '{0}'
                """.format(data.get('second_group'))

            if(data.get('main_group')!= 'all'):
                filters = filters + """
                AND pos_cat2.name->>'en_US' = '{0}'
                """.format(data.get('main_group'))
            
            if(data.get('bond_number')!= 'all'):
                filters = filters + """
                AND stock_picking.name = '{0}'
                """.format(data.get('bond_number'))
            
            if(data.get('exports_from')!= 'all'):
                filters = filters + """
                AND wh1.id = '{0}'
                """.format(data.get('exports_from'))

            if(data.get('imports_to')!= 'all'):
                filters = filters + """
                AND wh2.id = '{0}'
                """.format(data.get('imports_to'))
            
            if(data.get('bond_type')):
                if(data.get('bond_type')!= 'all'):
                    filters = filters + """
                    AND stock_picking_type.name->>'ar_001' = '{0}'
                    """.format(data.get('bond_type'))
            if(data.get('bond_type_sales')):
                if(data.get('bond_type_sales') == "all"):
                    filters = filters + """
                    AND stock_picking_type.code IN ('incoming', 'outgoing')
                    """               
                else:
                    filters = filters + """
                    AND stock_picking_type.code = '{0}'
                    """.format(data.get('bond_type_sales'))
            else:
                filters = filters + """
                AND stock_picking_type.code IN ('incoming', 'outgoing')
                """               

            trimmed_filters = filters.lstrip()

            if trimmed_filters.startswith("AND"):
                filters = "WHERE " + trimmed_filters[3:]

            query = \
                '''
                SELECT subq.file_name,
                    subq.picking_id,
                    subq.product_id,
                    subq.reference,
                    prod.default_code AS product_code,
                    uom.name->>'en_US' AS product_uom_name,
                    subq.qty_done,
                    loc1.name AS location_id_name,
                    loc2.name AS location_dest_id_name,
                    DATE(subq.date),
                    stock_picking.name AS pick_name,
                    stock_picking.origin,
                    stock_picking.picking_type_id,
                    stock_picking_type.name->>'ar_001' AS picking_type_name,
                    stock_picking_type.code,
                    pos_cat1.x_studio_name_in_ar AS pos_category_name,
                    pos_cat2.name->>'en_US' AS pos_category_parent_name,
                    CASE 
						WHEN loc1.id = 14 THEN 'جرد'
						ELSE wh1.name 
					END AS warehouse_id_name,

                    CASE 
						WHEN loc1.id = 4 AND loc2.id <> 4   THEN 'مرتجعات'
						ELSE 'مبيعات'
					END AS code,

                    CASE 
						WHEN loc2.id = 14 THEN 'عجز المخزون'
						ELSE wh2.name 
					END AS warehouse_dest_id_name
                FROM (
                    SELECT stock_move.name AS file_name,
                        stock_move.picking_id,
                        stock_move.reference,
                        stock_move_line.product_id,
                        stock_move_line.product_uom_id,
                        stock_move_line.qty_done,
                        stock_move_line.location_id,
                        stock_move_line.location_dest_id,
                        stock_move.date
                    FROM stock_move 
                    JOIN stock_move_line ON stock_move.id = stock_move_line.move_id 
                    WHERE stock_move.picking_id IS NOT NULL
                        AND stock_move.date BETWEEN '{0}' AND '{1}'
                ) AS subq
                JOIN stock_picking ON subq.picking_id = stock_picking.id
                JOIN stock_location AS loc1 ON subq.location_id = loc1.id
                JOIN stock_location AS loc2 ON subq.location_dest_id = loc2.id
                JOIN product_product AS prod ON subq.product_id = prod.id
                JOIN uom_uom AS uom ON subq.product_uom_id = uom.id
                JOIN stock_picking_type ON stock_picking.picking_type_id = stock_picking_type.id
                LEFT JOIN product_template AS prod_tmpl ON prod_tmpl.id = prod.product_tmpl_id
                LEFT JOIN pos_category AS pos_cat1 ON pos_cat1.id = prod_tmpl.pos_categ_id
                LEFT JOIN pos_category AS pos_cat2 ON pos_cat1.parent_id = pos_cat2.id
                LEFT JOIN stock_warehouse AS wh1 ON loc1.warehouse_id = wh1.id
                LEFT JOIN stock_warehouse AS wh2 ON loc2.warehouse_id = wh2.id
                {2}
                LIMIT {3} OFFSET {4};
                '''.format(date_from,date_to,filters,limited,counting)

            querycount =  '''
            SELECT COUNT(*) AS total_rows
            FROM 
                (
                    SELECT stock_move.name AS file_name,
                        stock_move.picking_id,
                        stock_move.reference,
                        stock_move_line.product_id,
                        stock_move_line.product_uom_id,
                        stock_move_line.qty_done,
                        stock_move_line.location_id,
                        stock_move_line.location_dest_id,
                        stock_move.date
                    FROM stock_move 
                    JOIN stock_move_line ON stock_move.id = stock_move_line.move_id 
                    WHERE stock_move.picking_id IS NOT NULL
                        AND stock_move.date BETWEEN '{0}' AND '{1}'
                ) AS subq
                JOIN stock_picking ON subq.picking_id = stock_picking.id
                JOIN stock_location AS loc1 ON subq.location_id = loc1.id
                JOIN stock_location AS loc2 ON subq.location_dest_id = loc2.id
                JOIN product_product AS prod ON subq.product_id = prod.id
                JOIN uom_uom AS uom ON subq.product_uom_id = uom.id
                JOIN stock_picking_type ON stock_picking.picking_type_id = stock_picking_type.id
                LEFT JOIN product_template AS prod_tmpl ON prod_tmpl.id = prod.product_tmpl_id
                LEFT JOIN pos_category AS pos_cat1 ON pos_cat1.id = prod_tmpl.pos_categ_id
                LEFT JOIN pos_category AS pos_cat2 ON pos_cat1.parent_id = pos_cat2.id
                LEFT JOIN stock_warehouse AS wh1 ON loc1.warehouse_id = wh1.id
                LEFT JOIN stock_warehouse AS wh2 ON loc2.warehouse_id = wh2.id
            ;
            '''.format(date_from,date_to)
            self._cr.execute(querycount)
            report_number_pages = self._cr.dictfetchall()[0]
            report_sub_lines.append(report_number_pages)   
       
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
        
        if(len(report_res) == 2):
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res[1], 'count': report_res[0], 'limited': data.get('limited')}
        else:
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': self._get_report_sub_lines(data, date_from, date_to), 'count': 0,'limited': 25}
        # else:
        #     report_res = self._get_report_sub_lines(data, date_from, date_to)
        
        # return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}