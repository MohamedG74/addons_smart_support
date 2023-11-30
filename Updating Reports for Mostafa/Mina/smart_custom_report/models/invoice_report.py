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



class DynamicInvoiceReport(models.Model):

    _name = 'dynamic.invoice.report'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    date_from = fields.Date('Start Date')
    date_to = fields.Date('End Date')
    main_group=fields.Char(string='Group')
    second_group=fields.Char(string='Second Group')

    department_id=fields.Char(string='Department')
   

    @api.model
    def purchase_report(self, option):
        orders = self.env['purchase.order'].search([])
        report_values = self.env['dynamic.invoice.report'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        if report_values.department_id:
            data.update({'department_id': report_values.department_id})
        
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
        
        
        department_id = '''
            SELECT
                department_id, hr_department.name
            FROM
                hr_employee
            LEFT JOIN hr_department on hr_employee.department_id = hr_department.id
            WHERE department_id is not null
        '''
        department = self._cr.execute(department_id)
        department_output = self._cr.dictfetchall() 
        
       
       
        return {
            'name': 'Invoice Report',
            'type': 'ir.actions.client',
            'tag': 'i_e_r',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'groups':main_group_output,
            'departments':department_output,
            'filters': filters,
            'report_lines': lines,
            }
   
    @api.model
    def generate_report(self,date_from,date_to, department_id):
        
        self.env.cr.execute("""
            SELECT 
                he.name as employee_name,
                hr_department.name as department_id,
                COUNT(CASE WHEN am.move_type = 'out_invoice' THEN 1 ELSE NULL END) AS invoice_count,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total ELSE 0 END) AS total_sales,
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total ELSE 0 END) AS total_returns,
                (SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total ELSE 0 END) - 
                 SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total ELSE 0 END)) AS net_sales,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_total - am.amount_residual ELSE 0 END) - 
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_total - am.amount_residual ELSE 0 END) AS total_paid,
                SUM(CASE WHEN am.move_type = 'out_invoice' THEN am.amount_residual ELSE 0 END) - 
                SUM(CASE WHEN am.move_type = 'out_refund' THEN am.amount_residual ELSE 0 END) AS not_paid
            FROM 
                account_move am
            JOIN 
                hr_employee he ON am.x_studio_employee = he.id
            LEFT JOIN hr_department on he.department_id = hr_department.id
            WHERE 
                am.x_studio_employee IS NOT NULL
                AND he.department_id IS NOT NULL
                AND hr_department.name='المندوبين'
                AND am.date >= %s AND am.date <= %s
            GROUP BY 
                am.x_studio_employee, he.name, hr_department.name;
            """, ( date_from, date_to))

        result = self.env.cr.fetchall()
        report_lines_vals = []
        for row in result:
            report_lines_vals.append({
                'employee_name': row[0],
                'department_id': row[1],
                'invoice_count': row[2],
                'total_sales': row[3],
                'total_returns': row[4],
                'net_sales': row[5],
                'total_paid': row[6],
                'not_paid': row[7],
                
            })

        return report_lines_vals
      

    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.invoice.report'].search([('id', '=',option[0])])
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
        department_id = data.get('department_id')
        report_sub_lines = []
        new_filter = None
        query = ""
        filters=""

        # if data.get('date_from') and data.get('date_to') and data.get('report_location')!='all':
        if data.get('date_from') and data.get('date_to'):
            return [self.generate_report(data.get('date_from'), data.get('date_to'), data.get('department_id'))]
        
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
