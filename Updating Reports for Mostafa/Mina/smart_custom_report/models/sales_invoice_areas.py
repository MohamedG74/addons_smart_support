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


class DynamicSalesInvoiceAreas(models.Model):

    _name = 'dynamic.sales.invoice.areas'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_product = fields.Char(string='Report Product') 
    invoice_number=fields.Char(string='Invoice Number')
    invoice_type=fields.Selection([('all','all'),('out_invoice','Customer Invoice'),
                                    ('out_refund','Customer Credit Note'),],string='Invoice Type')
    
    report_area=fields.Selection([('all','all'),('الجنوبية','الجنوبية'),('الرياض','الرياض'),
                                    ('الشرقية','الشرقية'),('الشمالية','الشمالية'),('الغربية','الغربية'),('القصيم','القصيم'),],string='المنطقة')
    report_location = fields.Char(string='Report Location')

    res_user=fields.Char(string='User')
    res_partner=fields.Char(string='Partner')
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
        report_values = self.env['dynamic.sales.invoice.areas'].search([('id', '=', option[0])])
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
        
        if report_values.report_area:
            data.update({'report_area': report_values.report_area})        
        
        if report_values.res_user:
            data.update({'res_user': report_values.res_user})
        if report_values.res_partner:
            data.update({'res_partner': report_values.res_partner})
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
        

        product_name = '''
            SELECT
                product_product.id, product_product.default_code, product_template.name->>'en_US' AS name
            FROM
                product_product
            LEFT JOIN product_template ON product_product.id = product_template.id;
        '''
        prod = self._cr.execute(product_name)
        product_output = self._cr.dictfetchall()
        

        branch_name = '''
            SELECT
                id,name,report_area
            FROM
                operating_unit
            WHERE report_area is not null
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
            WHERE customer_rank > 0;
        '''
        partner = self._cr.execute(res_partner)
        res_partner_output = self._cr.dictfetchall() 


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
            'name': 'Sales Invoice Areas',
            'type': 'ir.actions.client',
            'tag': 's_i_a',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'branch': branch_output,
            'user': res_user_output,
            'partner':res_partner_output,
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
        r = self.env['dynamic.sales.invoice.areas'].search([('id', '=',option[0])])
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
            


            if(data.get('report_area')):
                if(data.get('report_area') == "all"):
                    filters = filters + """
                    AND operating_unit.report_area IN ('الجنوبية', 'الرياض','الشرقية','الشمالية','الغربية','القصيم','all')
                    """               
                else:
                    filters = filters + """
                    AND operating_unit.report_area = '{0}'
                    """.format(data.get('report_area'))
            else:
                filters = filters + """
                AND operating_unit.report_area IN ('الجنوبية', 'الرياض','الشرقية','الشمالية','الغربية','القصيم','all')
                """               




            if(data.get('invoice_number')!='all'):
                filters = filters + """
                AND account_move.name = '{0}'
                """.format(data.get('invoice_number'))
            
            if(data.get('res_user') !='all'):#المستخدم
                filters = filters + """
                AND res_partner_user.name = '{0}'
                """.format(data.get('res_user'))
             
            if(data.get('res_partner')!= 'all'):#العميل
                filters = filters + """
                AND res_partner.name = '{0}'
                """.format(data.get('res_partner'))
            

            if(data.get('report_location')!= 'all'):#المستودع
                filters = filters + """
                AND operating_unit.name = '{0}'
                """.format(data.get('report_location'))

            if(data.get('hr_employee')!= 'all'):#مندوب المبيعات
                filters = filters + """
                AND hr_employee.name = '{0}'
                """.format(data.get('hr_employee'))


            query = \
                '''
                SELECT 
                    res_partner.name AS partner_name, 
                    account_move.name,
                    hr_employee.name AS employee_name, 
                    operating_unit.name AS branch_name, 
                    operating_unit.report_area AS report_area, 
                    res_partner_user.name AS user_name,
                    CASE 
                        WHEN account_move.move_type = 'out_invoice' THEN 'بيع'
                        WHEN account_move.move_type = 'out_refund' THEN 'مرتجع بيع'
                    END AS move_type,
                    account_move.invoice_date, 
                    COALESCE(account_move.stot_disc_before,account_move.amount_untaxed) as stot_disc_before, 
                    COALESCE(account_move.stot_disc,0) as stot_disc, 
                    account_move.amount_untaxed, 
                    account_move.amount_tax, 
                    account_move.amount_total
                FROM 
                    account_move 
                LEFT JOIN 
                    res_partner 
                ON 
                    res_partner.id = account_move.partner_id 
                LEFT JOIN 
                    hr_employee 
                ON 
                    hr_employee.id = account_move.x_studio_employee 
                LEFT JOIN 
                    operating_unit 
                ON 
                    operating_unit.id = account_move.x_studio_branch 
                LEFT JOIN 
                    res_users 
                ON 
                    res_users.id = account_move.invoice_user_id 
                LEFT JOIN
                    res_partner AS res_partner_user
                ON 
                    res_partner_user.id = res_users.partner_id
                WHERE 
                    account_move.invoice_date BETWEEN '{0}' AND '{1}'
                    {2}
                    AND state  = 'posted'
                ORDER BY invoice_date DESC
                LIMIT {3} OFFSET {4};
                '''.format(date_from,date_to,filters,limited,counting)
            

            querycount =  '''
            SELECT COUNT(*) AS total_rows
            FROM 
                    account_move 
                LEFT JOIN 
                    res_partner 
                ON 
                    res_partner.id = account_move.partner_id 
                LEFT JOIN 
                    hr_employee 
                ON 
                    hr_employee.id = account_move.x_studio_employee 
                LEFT JOIN 
                    operating_unit 
                ON 
                    operating_unit.id = account_move.x_studio_branch 
                LEFT JOIN 
                    res_users 
                ON 
                    res_users.id = account_move.invoice_user_id 
                LEFT JOIN
                    res_partner AS res_partner_user
                ON 
                    res_partner_user.id = res_users.partner_id
                WHERE 
                    account_move.invoice_date BETWEEN '{0}' AND '{1}'
                    {2}
                    AND state  = 'posted'
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
                    operating_unit.report_area AS report_area, 
                    res_partner_user.name AS user_name,
                    CASE 
                        WHEN account_move.move_type = 'out_invoice' THEN 'بيع'
                        WHEN account_move.move_type = 'out_refund' THEN 'مرتجع بيع'
                    END AS move_type,
                    account_move.invoice_date, 
                    COALESCE(account_move.stot_disc_before,account_move.amount_untaxed) as stot_disc_before, 
                    COALESCE(account_move.stot_disc,0) as stot_disc, 
                    account_move.amount_untaxed, 
                    account_move.amount_tax, 
                    account_move.amount_total
                FROM 
                    account_move 
                LEFT JOIN 
                    res_partner 
                ON 
                    res_partner.id = account_move.partner_id 
                LEFT JOIN 
                    hr_employee 
                ON 
                    hr_employee.id = account_move.x_studio_employee 
                LEFT JOIN 
                    operating_unit 
                ON 
                    operating_unit.id = account_move.x_studio_branch 
                LEFT JOIN 
                    res_users 
                ON 
                    res_users.id = account_move.invoice_user_id 
                LEFT JOIN
                    res_partner AS res_partner_user
                ON 
                    res_partner_user.id = res_users.partner_id
                WHERE 
                    account_move.move_type IN ('out_invoice', 'out_refund')
                    AND state  = 'posted'
                    ORDER BY invoice_date DESC
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
        
        # if(len(report_res) > 0):
        #     report_res = report_res[0]
        
        if(len(report_res) == 2):
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res[1], 'count': report_res[0], 'limited': data.get('limited')}
        else:
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': self._get_report_sub_lines(data, date_from, date_to), 'count': 0 ,'limited': 25}

        # else:
        #     report_res = self._get_report_sub_lines(data, date_from, date_to)
        
        # return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res}
