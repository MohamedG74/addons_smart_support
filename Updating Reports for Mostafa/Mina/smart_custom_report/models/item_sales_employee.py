#!/usr/bin/python
# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError
# from sqlalchemy import create_engine, text
import io
import json
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class DynamicItemSalesReturn(models.Model):

    _name = 'dynamic.item.sales.employee'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_product = fields.Char(string='Report Product') 
    invoice_number=fields.Char(string='Invoice Number')
    invoice_type=fields.Selection([('all','all'),('out_invoice','Customer Invoice'),
                                    ('out_refund','Customer Credit Note'),],string='Invoice Type')
    report_location = fields.Char(string='Report Location')

    res_user=fields.Char(string='User')
    res_partner=fields.Char(string='Partner')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')
    hr_employee=fields.Char(string='Employee')
    counting=fields.Char(string='Counting')
    

    limited=fields.Integer(string='Limited')

    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    # report_type = fields.Selection([('report_by_order',
    #                                'Report By Order'),
    #                                ('report_by_product',
    #                                'Report By Product')],
    #                                default='report_by_order')

    @api.model
    def purchase_report(self, option):
        report_values = self.env['dynamic.item.sales.employee'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        
        if report_values.invoice_number:
            data.update({'invoice_number': report_values.invoice_number})
        else:
            data.update({'invoice_number': "all"})

        if report_values.invoice_type:
            data.update({'invoice_type': report_values.invoice_type})        
        if report_values.res_user:
            data.update({'res_user': report_values.res_user})
        if report_values.res_partner:
            data.update({'res_partner': report_values.res_partner})    
        if report_values.main_group:
            data.update({'main_group': report_values.main_group})    
        if report_values.second_group:
            data.update({'second_group': report_values.second_group})    
        if report_values.hr_employee:
            data.update({'hr_employee': report_values.hr_employee})
        
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
        
        branch_name = '''
            SELECT
                id,name
            FROM
                operating_unit
        '''
        branch = self._cr.execute(branch_name)
        branch_output = self._cr.dictfetchall()    

        res_user = '''
            SELECT
                res_users.id, res_users.partner_id, res_partner.name
            FROM
                res_users
            LEFT JOIN res_partner ON res_users.partner_id = res_partner.id
        '''
        user = self._cr.execute(res_user)
        res_user_output = self._cr.dictfetchall()  
        

        res_partner = '''
            SELECT
                res_partner.id, res_partner.name
            FROM
                res_partner
            WHERE supplier_rank > 0;
        '''
        partner = self._cr.execute(res_partner)
        res_partner_output = self._cr.dictfetchall() 

        main_group = '''
            SELECT
                id,name->>'en_US' as name ,x_studio_name_in_ar as namear
            FROM
                pos_category
        '''
        group = self._cr.execute(main_group)
        main_group_output = self._cr.dictfetchall() 

        hr_employee = '''
            SELECT
                id,name
            FROM
                hr_employee
            WHERE department_id = 3;
        '''
        employee = self._cr.execute(hr_employee)
        hr_employee_output = self._cr.dictfetchall()

        count = self._get_report_values(data).get('count')
        limited = self._get_report_values(data).get('limited')
        return {
            'name': 'Item Sales Employee',
            'type': 'ir.actions.client',
            'tag': 'i_t_e',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'branch': branch_output,
            'user': res_user_output,
            'partner':res_partner_output,
            'groups':main_group_output,
            'employee':hr_employee_output,
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
        r = self.env['dynamic.item.sales.employee'].search([('id', '=',option[0])])
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


        if data.get('date_from') and data.get('date_to'):
            if(data.get('invoice_type')):
                if(data.get('invoice_type') == "all"):
                    filters = filters + """
                    AND account_move.move_type IN ('out_invoice', 'out_refund')
                    """               
                else:
                    filters = filters + """
                    AND account_move.move_type = '{0}'
                    """.format(data.get('invoice_type'))
            else:
                filters = filters + """
                AND account_move.move_type IN ('out_invoice', 'out_refund')
                """               

            if(data.get('invoice_number')!='all'):
                filters = filters + """
                AND account_move.name = '{0}'
                """.format(data.get('invoice_number'))
            
            if(data.get('res_user') !='all'):
                filters = filters + """
                AND res_partner_user.name = '{0}'
                """.format(data.get('res_user'))
             

            if(data.get('res_partner')!= 'all'):
                filters = filters + """
                AND res_partner.name = '{0}'
                """.format(data.get('res_partner'))
            
            if(data.get('report_location')!= 'all'):
                filters = filters + """
                AND operating_unit.name = '{0}'
                """.format(data.get('report_location'))
            
            if(data.get('hr_employee')!= 'all'):#مندوب المبيعات
                filters = filters + """
                AND hr_employee.name = '{0}'
                """.format(data.get('hr_employee'))

            if(data.get('report_product')!= 'all'):
                filters = filters + """
                AND product_template.name->>'en_US' = '{0}'
                """.format(data.get('report_product'))
            
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
                    res_partner.name AS partner_name, 
                    hr_employee.name AS employee_name, 
                    account_move.name,
                    operating_unit.name AS branch_name, 
                    res_partner_user.name AS user_name,
                    CASE 
                        WHEN account_move.move_type = 'out_invoice' THEN 'بيع'
                        WHEN account_move.move_type = 'out_refund' THEN 'مرتجع بيع'
                    END AS move_type,
                    account_move.invoice_date,
                    account_move_line.product_id,
                    account_move.amount_total,
                    account_move_line.price_unit,
                    account_move_line.quantity,
                    uom_uom.name->>'en_US' AS product_uom_name,
                    (account_move_line.price_subtotal+(account_move_line.discount * account_move_line.price_subtotal) / 100) AS before_discount,
                    ((account_move_line.discount * account_move_line.price_subtotal) / 100) AS discount_value,
                    account_move_line.discount AS discount_percent,
                    account_move_line.price_subtotal,
                    (account_move_line.price_total - account_move_line.price_subtotal) AS price_tax,
                    account_move_line.price_total,
                    pc1.x_studio_name_in_ar AS category_name,
                    pc2.name->>'en_US' AS parent_category_name,
                    product_template.default_code,
	                product_template.name->>'en_US' as prodcut_name,

                    (account_move_line.price_subtotal + (account_move_line.price_total - account_move_line.price_subtotal)) AS subtotal_with_tax_sum

                FROM 
                    account_move 
                    JOIN res_partner ON res_partner.id = account_move.partner_id 
                    LEFT JOIN hr_employee ON hr_employee.id = account_move.x_studio_employee 
                    JOIN operating_unit ON operating_unit.id = account_move.x_studio_branch 
                    JOIN res_users ON res_users.id = account_move.invoice_user_id 
                    JOIN res_partner AS res_partner_user ON res_partner_user.id = res_users.partner_id
                    JOIN account_move_line ON account_move_line.move_id = account_move.id
                    JOIN uom_uom ON uom_uom.id = account_move_line.product_uom_id
                    LEFT JOIN product_product ON product_product.id = account_move_line.product_id
                    LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                    LEFT JOIN pos_category pc1 ON product_template.pos_categ_id = pc1.id
                    LEFT JOIN pos_category pc2 ON pc1.parent_id = pc2.id
                WHERE 
                    account_move_line.product_id IS NOT NULL
                    AND account_move_line.name <> '[DISC] Discount'
                    AND account_move_line.name <> '[Discount] Discount'
                    AND hr_employee.name IS NOT NULL
                    AND account_move.invoice_date BETWEEN '{0}' AND '{1}'
                    AND account_move_line.display_type <> 'cogs'
                    AND account_move_line.display_type <> 'epd'
                    {2}
                    LIMIT {3} OFFSET {4};
                '''.format(date_from,date_to,filters,limited,counting)
            
            querycount =  '''
            SELECT COUNT(*) AS total_rows
            FROM 
                account_move 
                JOIN res_partner ON res_partner.id = account_move.partner_id 
                LEFT JOIN hr_employee ON hr_employee.id = account_move.x_studio_employee 
                JOIN operating_unit ON operating_unit.id = account_move.x_studio_branch 
                JOIN res_users ON res_users.id = account_move.invoice_user_id 
                JOIN res_partner AS res_partner_user ON res_partner_user.id = res_users.partner_id
                JOIN account_move_line ON account_move_line.move_id = account_move.id
                JOIN uom_uom ON uom_uom.id = account_move_line.product_uom_id
                LEFT JOIN product_product ON product_product.id = account_move_line.product_id
                LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                LEFT JOIN pos_category pc1 ON product_template.pos_categ_id = pc1.id
                LEFT JOIN pos_category pc2 ON pc1.parent_id = pc2.id
            WHERE 
                account_move_line.product_id IS NOT NULL
                AND account_move_line.name <> '[DISC] Discount'
                AND account_move_line.name <> '[Discount] Discount'
                AND hr_employee.name IS NOT NULL
                AND account_move.invoice_date BETWEEN '{0}' AND '{1}'
                AND account_move_line.display_type <> 'cogs'
                AND account_move_line.display_type <> 'epd'
                {2};
            '''.format(date_from,date_to,filters)
            
            self._cr.execute(querycount)
            report_number_pages = self._cr.dictfetchall()[0]
            report_sub_lines.append(report_number_pages)


            
        else:
            query = \
                '''
                SELECT 
                    res_partner.name AS partner_name, 
                    hr_employee.name AS employee_name, 
                    account_move.name,
                    operating_unit.name AS branch_name, 
                    res_partner_user.name AS user_name,
                    CASE 
                        WHEN account_move.move_type = 'out_invoice' THEN 'بيع'
                        WHEN account_move.move_type = 'out_refund' THEN 'مرتجع بيع'
                    END AS move_type,
                    account_move.invoice_date,
                    account_move_line.product_id,
                    account_move.amount_total,
                    account_move_line.price_unit,
                    account_move_line.quantity,
                    uom_uom.name->>'en_US' AS product_uom_name,
                    (account_move_line.price_subtotal+(account_move_line.discount * account_move_line.price_subtotal) / 100) AS before_discount,
                    ((account_move_line.discount * account_move_line.price_subtotal) / 100) AS discount_value,
                    account_move_line.discount AS discount_percent,
                    account_move_line.price_subtotal,
                    (account_move_line.price_total - account_move_line.price_subtotal) AS price_tax,
                    account_move_line.price_total,
                    pc1.x_studio_name_in_ar AS category_name,
                    pc2.name->>'en_US' AS parent_category_name,
                    product_template.default_code,
	                product_template.name->>'en_US' as prodcut_name,

                    (account_move_line.price_subtotal + (account_move_line.price_total - account_move_line.price_subtotal)) AS subtotal_with_tax_sum

                FROM 
                    account_move 
                    JOIN res_partner ON res_partner.id = account_move.partner_id 
                    LEFT JOIN hr_employee ON hr_employee.id = account_move.x_studio_employee 
                    JOIN operating_unit ON operating_unit.id = account_move.x_studio_branch 
                    JOIN res_users ON res_users.id = account_move.invoice_user_id 
                    JOIN res_partner AS res_partner_user ON res_partner_user.id = res_users.partner_id
                    JOIN account_move_line ON account_move_line.move_id = account_move.id
                    JOIN uom_uom ON uom_uom.id = account_move_line.product_uom_id
                    LEFT JOIN product_product ON product_product.id = account_move_line.product_id
                    LEFT JOIN product_template ON product_template.id = product_product.product_tmpl_id
                    LEFT JOIN pos_category pc1 ON product_template.pos_categ_id = pc1.id
                    LEFT JOIN pos_category pc2 ON pc1.parent_id = pc2.id
                WHERE 
                    account_move.move_type IN ('out_invoice', 'out_refund')
                    AND account_move_line.product_id IS NOT NULL
                    AND account_move_line.name <> '[DISC] Discount'
                    AND account_move_line.name <> '[Discount] Discount'
                    AND hr_employee.name IS NOT NULL

                    AND account_move_line.display_type <> 'cogs'
                    AND account_move_line.display_type <> 'epd'
                LIMIT {0} OFFSET {1};
                '''.format(limited,counting)
            
            querycount =  '''
            SELECT COUNT(*) AS total_rows
            FROM 
                account_move 
            
            WHERE 
           account_move.move_type IN ('in_invoice', 'in_refund')
            AND state = 'posted';
            '''
            self._cr.execute(querycount)
            report_number_pages = self._cr.dictfetchall()[0]
            report_sub_lines.append(report_number_pages)

       
        if(query != ""):
            self._cr.execute(query)
            report_by_order = self._cr.dictfetchall()
            report_sub_lines.append(report_by_order)
        
        return report_sub_lines


    def _get_report_values(self, data):
        docs = data['model']
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        report_res = self._get_report_sub_lines(data,date_from, date_to)
        
        # if(len(report_res) > 0):
        #     report_res = report_res[0]

        if(len(report_res) == 2):
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res[1], 'count': report_res[0], 'limited': data.get('limited')}
        else:
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': self._get_report_sub_lines(data, date_from, date_to), 'count': 0 ,'limited': 25}

        # else:
        #     report_res = self._get_report_sub_lines(data, date_from, date_to)
        
        # return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}
