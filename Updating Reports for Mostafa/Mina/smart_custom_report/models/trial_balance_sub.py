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
import datetime

class DynamicItemPurchaseReturn(models.Model):

    _name = 'dynamic.trial.balance.sub'
    
    purchase_report = fields.Char(string='Purchase Report')
    report_location = fields.Char(string='Report Location')
    report_product = fields.Char(string='Report Product')
    report_code = fields.Char(string='Account Code')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date to')
    account_name=fields.Char(string='Account Name')
    level=fields.Selection([('all','فرعى'),
                            ('level_1','المستوي الأول'),
                            ('level_2','المستوي الثاني'),
                            ('level_3','المستوي الثالث'),
                            ('level_4','المستوي الرابع'),
                            ('level_5','المستوي الخامس'),
                            ('level_6','المستوي السادس'),
                            ('level_7','المستوي التحليلى'),
                            ],string='Level')
    
    
    # report_type = fields.Selection([('report_by_order',
    #                                'Report By Order'),
    #                                ('report_by_product',
    #                                'Report By Product')],
    #                                default='report_by_order')

    @api.model
    def purchase_report(self, option):
        report_values = self.env['dynamic.trial.balance.sub'].search([('id', '=', option[0])])
        data = {'model': self}
        if report_values.date_from:
            data.update({'date_from': report_values.date_from})
        if report_values.date_to:
            data.update({'date_to': report_values.date_to})
        if report_values.report_location:
            data.update({'report_location': report_values.report_location})
        if report_values.report_code:
            data.update({'report_code': report_values.report_code})
        if report_values.report_product:
            data.update({'report_product': report_values.report_product})
        if report_values.account_name:
            data.update({'account_name': report_values.account_name})
        if report_values.level:
            data.update({'level': report_values.level})

        filters = self.get_filter(option)
        lines = self._get_report_values(data).get('PURCHASE')
        linesprev = self._get_report_values(data).get('PREVIOUS')
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
        


        account_name = '''
            SELECT
                id,name->>'en_US' as name,code 
            FROM
                account_account
            ORDER BY code                
        '''
        acc = self._cr.execute(account_name)
        account_name_output = self._cr.dictfetchall()


        return {
            'name': 'Purchase Orders',
            'type': 'ir.actions.client',
            'tag': 't_b_s',
            'orders': data,
            'locations':resul,
            'products':product_output,
            'accounts': account_name_output,
            'filters': filters,
            'report_lines': lines,
            'previous': linesprev,
            }


    def get_filter(self, option):
        data = self.get_filter_data(option)
        filters = {}
        return filters


    def get_filter_data(self, option):
        r = self.env['dynamic.trial.balance.sub'].search([('id', '=',option[0])])
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
        code = data.get('report_code')
        level = data.get('level')
        report_sub_lines = []
        new_filter = None
        query = ""
        query_prev = ""

        if data.get('date_from') and data.get('date_to') and data.get('report_code') and data.get('level') == 'all' :
            query = \
                '''
                SELECT 
                aa.code,
                aa.name->>'en_US' as name,
                ob.account_id,
                CASE WHEN LEFT(aa.code, 1) IN ('3','4') THEN 0 ELSE ob.opening_debit END AS opening_debit,
                CASE WHEN LEFT(aa.code, 1) IN ('3','4') THEN 0 ELSE ob.opening_credit END AS opening_credit,
                COALESCE(tr.transactions_debit,0) as transactions_debit,
                COALESCE(tr.transactions_credit,0) as transactions_credit,
                COALESCE(COALESCE(ob.opening_debit,0) + COALESCE(tr.transactions_debit,0),0) AS total_debit,
                COALESCE(COALESCE(ob.opening_debit,0) + COALESCE(tr.transactions_debit,0),0) AS total_debit,
                (CASE WHEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) >= 0 THEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) ELSE 0 END) AS debit_balance,
                (CASE WHEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) < 0 THEN -(COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) ELSE 0 END) AS credit_balance

                FROM (
                SELECT 
                    account_id, 
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) >= 0 
                        THEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) 
                        ELSE 0 
                    END AS opening_debit,
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) < 0 
                        THEN ABS(COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0)) 
                        ELSE 0 
                    END AS opening_credit
                FROM account_move_line
                WHERE date < '{0}'
                GROUP BY account_id
                ) ob
                LEFT JOIN (
                SELECT 
                    account_id, 
                    COALESCE(SUM(debit), 0) AS transactions_debit,
                    COALESCE(SUM(credit), 0) AS transactions_credit
                FROM account_move_line
                WHERE date BETWEEN '{0}' AND '{1}'
                GROUP BY account_id
                ) tr
                ON ob.account_id = tr.account_id
                LEFT JOIN account_account aa ON ob.account_id = aa.id
                LEFT JOIN account_move_line aml ON ob.account_id = aml.account_id
                WHERE LENGTH(aa.code) = 14
                AND aa.code LIKE '{2}%'
                GROUP BY aa.code,aa.name, ob.account_id, ob.opening_debit, ob.opening_credit, tr.transactions_debit, tr.transactions_credit;

                '''.format(date_from,date_to,code)
        elif data.get('date_from') and data.get('date_to') and data.get('level') != 'all' and data.get('level') != 'level_7':
            filters = ""
            if data.get('level') == 'level_1':
                filters = 2
            if data.get('level') == 'level_2':
                filters = 4
            if data.get('level') == 'level_3':
                filters = 6
            if data.get('level') == 'level_4':
                filters = 8
            if data.get('level') == 'level_5':
                filters = 10
            if data.get('level') == 'level_6':
                filters = 14
            #previous earning calculation
            date_str = data.get('date_from')
            # parse the date string into a datetime object
            date_obj = date_str.date()
            # get the year of the date object
            year = date_obj.year
            # calculate the start date of the previous year
            start_date = datetime.date(year-1, 1, 1)
            # calculate the end date of the previous year
            end_date = datetime.date(year-1, 12, 31)
            query_prev = \
            '''
            SELECT SUM(x.opening_credit)-SUM(x.opening_debit) as previous_earning FROM (
            SELECT
            account_account.account_type,
            CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) >= 0 
                THEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) 
                ELSE 0 
            END AS opening_debit,
            CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) < 0 
                THEN ABS(COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0)) 
                ELSE 0 
            END AS opening_credit
            FROM account_move_line
            LEFT JOIN 
            account_account 
            ON account_account.id = account_move_line.account_id
            WHERE date BETWEEN '{0}' and '{1}'
            AND (account_account.group_id IN (10,11,12) OR account_account.x_studio_filter_tpe_1 = 'other' 
                OR account_account.account_type IN('expense','expense_depreciation','expense_direct_cost') 
                )
            GROUP BY account_account.account_type
            ) x
            '''.format(start_date,end_date)

            query = \
            '''
                SELECT
                prefix as code,
				CASE WHEN LEFT(prefix, 1) IN ('3','4') THEN 0 ELSE COALESCE(SUM(COALESCE(ob.opening_debit, 0)), 0) END AS opening_debit,
                CASE WHEN LEFT(prefix, 1) IN ('3','4') THEN 0 ELSE COALESCE(SUM(COALESCE(ob.opening_credit, 0)), 0) END AS opening_credit,
                COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) AS transactions_debit,
                COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0) AS transactions_credit,
                CASE WHEN LEFT(prefix, 1) IN ('3','4') THEN COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) ELSE COALESCE(SUM(COALESCE(ob.opening_debit, 0) + COALESCE(tr.transactions_debit, 0)), 0) END AS total_debit,
                CASE WHEN LEFT(prefix, 1) IN ('3','4') THEN COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0) ELSE COALESCE(SUM(COALESCE(ob.opening_credit, 0) + COALESCE(tr.transactions_credit, 0)), 0) END AS total_credit,
                CASE WHEN LEFT(prefix, 1) IN ('3','4') 
                THEN 
                    CASE
                        WHEN 0 + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) >= 0 + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        THEN 0 + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) - 0 - COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        ELSE 0
                    END 
                ELSE 
                    CASE
                        WHEN COALESCE(SUM(COALESCE(ob.opening_debit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) >= COALESCE(SUM(COALESCE(ob.opening_credit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        THEN COALESCE(SUM(COALESCE(ob.opening_debit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) - COALESCE(SUM(COALESCE(ob.opening_credit, 0)), 0) - COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        ELSE 0
                    END 
                END AS debit_balance,

                CASE WHEN LEFT(prefix, 1) IN ('3','4') 
                THEN 
                    CASE
                        WHEN 0 + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) < 0 + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        THEN 0 + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0) - 0 - COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0)
                        ELSE 0
                    END 
                ELSE 
                    CASE
                        WHEN COALESCE(SUM(COALESCE(ob.opening_debit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0) < COALESCE(SUM(COALESCE(ob.opening_credit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0)
                        THEN COALESCE(SUM(COALESCE(ob.opening_credit, 0)), 0) + COALESCE(SUM(COALESCE(tr.transactions_credit, 0)), 0) - COALESCE(SUM(COALESCE(ob.opening_debit, 0)), 0) - COALESCE(SUM(COALESCE(tr.transactions_debit, 0)), 0)
                        ELSE 0
                    END 
                END AS credit_balance,

                (
                    SELECT name->>'en_US' as account_name
                    FROM account_account
                    WHERE account_account.code = prefix 
                    LIMIT 1
                ) AS name
                FROM (
                SELECT
                    code AS prefix,
                    id AS account_id
                FROM account_account
                WHERE LENGTH(code) = 14
                ) aa
                LEFT JOIN (
                SELECT
                    account_id,
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) >= 0 
                        THEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) 
                        ELSE 0 
                    END AS opening_debit,
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) < 0 
                        THEN ABS(COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0)) 
                        ELSE 0 
                    END AS opening_credit
                FROM account_move_line
                WHERE date < '{0}'
                
                GROUP BY account_id
                ) ob ON aa.account_id = ob.account_id
                LEFT JOIN (
                SELECT
                    account_id,
                    COALESCE(SUM(CASE WHEN debit > 0 THEN debit ELSE 0 END), 0) AS transactions_debit,
                    COALESCE(SUM(CASE WHEN credit > 0 THEN credit ELSE 0 END), 0) AS transactions_credit
                FROM account_move_line
                WHERE date BETWEEN '{0}' AND '{1}' 

                                GROUP BY account_id
                ) tr ON aa.account_id = tr.account_id
                GROUP BY prefix;

            '''.format(date_from,date_to,filters)

        elif data.get('date_from') and data.get('date_to') and data.get('level') == 'level_7':
           query = \
                '''
                SELECT 
                aa.code,
                aa.name->>'en_US' as name,
                ob.account_id,
                CASE WHEN LEFT(aa.code, 1) IN ('3','4') THEN 0 ELSE ob.opening_debit END AS opening_debit,
                CASE WHEN LEFT(aa.code, 1) IN ('3','4') THEN 0 ELSE ob.opening_credit END AS opening_credit,
                COALESCE(tr.transactions_debit,0) as transactions_debit,
                COALESCE(tr.transactions_credit,0) as transactions_credit,
                COALESCE(COALESCE(ob.opening_debit,0) + COALESCE(tr.transactions_debit,0),0) AS total_debit,
                COALESCE(COALESCE(ob.opening_debit,0) + COALESCE(tr.transactions_debit,0),0) AS total_debit,
                (CASE WHEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) >= 0 THEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) ELSE 0 END) AS debit_balance,
                (CASE WHEN (COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) < 0 THEN -(COALESCE((CASE WHEN ob.opening_debit > 0 THEN ob.opening_debit ELSE 0 END) - (CASE WHEN ob.opening_credit > 0 THEN ob.opening_credit ELSE 0 END), 0) + COALESCE((CASE WHEN tr.transactions_debit > 0 THEN tr.transactions_debit ELSE 0 END) - (CASE WHEN tr.transactions_credit > 0 THEN tr.transactions_credit ELSE 0 END), 0)) ELSE 0 END) AS credit_balance

                FROM (
                SELECT 
                    account_id, 
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) >= 0 
                        THEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) 
                        ELSE 0 
                    END AS opening_debit,
                    CASE WHEN COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0) < 0 
                        THEN ABS(COALESCE(SUM(debit), 0) - COALESCE(SUM(credit), 0)) 
                        ELSE 0 
                    END AS opening_credit
                FROM account_move_line
                WHERE date < '{0}' or (date = '{0}' and ref='opening2021')
                GROUP BY account_id
                ) ob
                LEFT JOIN (
                SELECT 
                    account_id, 
                    COALESCE(SUM(debit), 0) AS transactions_debit,
                    COALESCE(SUM(credit), 0) AS transactions_credit
                FROM account_move_line
                WHERE date BETWEEN '{0}' AND '{1}' AND ref <> 'opening2021'
                GROUP BY account_id
                ) tr
                ON ob.account_id = tr.account_id
                LEFT JOIN account_account aa ON ob.account_id = aa.id
                LEFT JOIN account_move_line aml ON ob.account_id = aml.account_id
                WHERE LENGTH(aa.code) = 14
                GROUP BY aa.code,aa.name, ob.account_id, ob.opening_debit, ob.opening_credit, tr.transactions_debit, tr.transactions_credit;

                '''.format(date_from,date_to)
        if(query != ""):
            self._cr.execute(query)
            report_by_order = self._cr.dictfetchall()
            report_sub_lines.append(report_by_order)
        if(query_prev != ""):
            self._cr.execute(query_prev)
            report_by_order = self._cr.dictfetchall()
            report_sub_lines.append(report_by_order)
            # print(report_by_order)

        
        return report_sub_lines


    def _get_report_values(self, data):
        docs = data['model']
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        report_res = self._get_report_sub_lines(data,date_from, date_to)
        #print(len(report_res))
        #if(len(report_res) > 0):
        #    report_res = report_res[0]
        # else:
        #     report_res = self._get_report_sub_lines(data, date_from, date_to)
        if(len(report_res) == 2):
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': report_res[0], 'PREVIOUS': report_res[1]}
        else:
            return {'doc_ids': self.ids, 'docs': docs, 'PURCHASE': self._get_report_sub_lines(data, date_from, date_to), 'PREVIOUS': []}


