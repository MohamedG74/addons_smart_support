# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import fields, models, _
from datetime import datetime
from odoo.exceptions import UserError
import csv
import base64
import xlrd
from odoo.tools import ustr
import traceback
import psycopg2
from psycopg2 import Error
import logging

class ImportINVWizard(models.TransientModel):
    _name = "import.inv.wizard"

    import_type = fields.Selection([
        ('csv', 'CSV File'),
        ('excel', 'Excel File')
    ], default="excel", string="Import File Type", required=True)
    file = fields.Binary(string="File", required=False)
    product_by = fields.Selection([
        ('name', 'Name'),
        ('int_ref', 'Internal Reference'),
        ('barcode', 'Barcode')
    ], default="name", string="Product By", required=True)
    invoice_type = fields.Selection([
        ('inv', 'Customer Invoice'),
        ('bill', 'Vendor Bill'),
        ('ccn', 'Customer Credit Note'),
        ('vcn', 'Vendor Credit Note')
    ], default="inv", string="Invoicing Type", required=True)
    is_validate = fields.Boolean(string="Auto Post?",default=True)
    inv_no_type = fields.Selection([
        ('auto', 'Auto'),
        ('as_per_sheet', 'As per sheet')
    ], default="as_per_sheet", string="Number", required=True)

    def show_success_msg(self, counter, validate_rec, skipped_line_no):
        # open the new success message box
        view = self.env.ref('sh_message.sh_message_wizard')
        context = dict(self._context or {})
        dic_msg = str(counter) + " Records imported successfully \n"
        dic_msg = dic_msg + str(validate_rec) + " Records Validate"
        if skipped_line_no:
            dic_msg = dic_msg + "\nNote:"
        for k, v in skipped_line_no.items():
            dic_msg = dic_msg + "\nRow No " + k + " " + v + " "
        context['message'] = dic_msg

        return {
            'name': 'Success',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'sh.message.wizard',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }

    def import_inv_apply(self):
        inv_obj = self.env['account.move']
        # perform import lead
        print("no")
        if self:
            print("yes")
            # For Excel
            if self.import_type == 'excel':
                logger = logging.getLogger('server_logger')
                logger.setLevel(logging.DEBUG)
                # create file handler which logs even debug messages
                fh = logging.FileHandler('importing.log')
                fh.setLevel(logging.DEBUG)
                # create console handler with a higher log level
                ch = logging.StreamHandler()
                ch.setLevel(logging.ERROR)
                # create formatter and add it to the handlers
                formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
                ch.setFormatter(formatter)
                fh.setFormatter(formatter)
                # add the handlers to logger
                logger.addHandler(ch)
                logger.addHandler(fh)

                logger.error("Importing Started.")

                counter = 1
                skipped_line_no = {}
                try:
                    running_inv = None
                    created_inv = False
                    created_inv_list_for_validate = []
                    created_inv_list = []
                    #new
                    connection = psycopg2.connect(user="openpg",
                                    password="openpgpwd",
                                    host="127.0.0.1",
                                    port="5432",
                                    database="Meshkati1")

                    connectiontwo = psycopg2.connect(user="openpg",
                                                password="openpgpwd",
                                                host="127.0.0.1",
                                                port="5432",
                                                database="mdata")
                    
                    # Create a cursor to perform database operations
                    cursor = connection.cursor()
                    #cursorsales = connectiontwo.cursor()
                    #cursorsales.itersize = 50 # chunk size

                    with connectiontwo.cursor(name='cursorsales') as curso:
                        
                        curso.itersize = 20    
                        curso.execute("SELECT * from sales_invoices LIMIT 2000")                
                        while True:
                            rows = curso.fetchmany(20)
                            if len(rows) > 0:
                                for rowinv in rows:
                                    cursortwo = connectiontwo.cursor()
                                    cursortwo.execute("SELECT * from sales_invoices_details WHERE \"Invid\" = %s ",(rowinv[1],))
                                    table_data =  cursortwo.fetchall()

                                    for num, row in enumerate(table_data):
                                        try:
                                            newcursor = connectiontwo.cursor()
                                            newcursor.execute("SELECT * from items WHERE itmid = '%s' ",(row[3],))
                                            first_row = newcursor.fetchone()
                                            #product
                                            odoocursor = connection.cursor()
                                            odoocursor.execute("SELECT * from product_template WHERE default_code = %s",(first_row[3],))
                                            item_odoo = odoocursor.fetchone()
                                            #branch
                                            odoocursorbr = connection.cursor()
                                            odoocursorbr.execute("select id from operating_unit where code =  '%s' ",(rowinv[7],))
                                            branch_odoo = odoocursorbr.fetchone()

                                            if rowinv[4] not in (None, "") and item_odoo[0] not in (None, ""):
                                                vals = {}
                                                
                                                if rowinv[4] != running_inv:
                                                                                                                        
                                                    running_inv = rowinv[4]
                                                    inv_vals = {}
                                                    partner_iodoo = "POS Agent"    
                                                    if partner_iodoo not in (None, ""):
                                                        partner_obj = self.env["res.partner"]
                                                        partner = partner_obj.search(
                                                            [('name', '=', partner_iodoo)], limit=1)

                                                        if partner:
                                                            inv_vals.update(
                                                                {'partner_id': partner.id})
                                                        else:
                                                            skipped_line_no[str(
                                                                counter)] = " - Customer/Vendor not found. "
                                                            counter = counter + 1
                                                            continue
                                                    else:
                                                        skipped_line_no[str(
                                                            counter)] = " - Customer/Vendor field is empty. "
                                                        counter = counter + 1
                                                        continue

                                                    if rowinv[13] not in (None, ""):
                                                        partner_objtwo = self.env["res.users"]
                                                        partnertwo = partner_objtwo.search(
                                                            [('name', '=', rowinv[13])], limit=1)

                                                        if partnertwo:
                                                            inv_vals.update(
                                                                {'invoice_user_id': partnertwo.id})
                                                        else:
                                                            skipped_line_no[str(
                                                                counter)] = " - User not found. "
                                                            counter = counter + 1
                                                            continue
                                                    else:
                                                        skipped_line_no[str(
                                                            counter)] = " - User field is empty. "
                                                        counter = counter + 1
                                                        continue    

                                                    if rowinv[5] not in (None, ""):
                                                        cd = rowinv[5]
                                                        cd = str(cd.strftime('%Y-%m-%d'))
                                                        inv_vals.update({'invoice_date': cd})

                                                    if branch_odoo not in (None, ""):
                                                        bran = branch_odoo[0]                                        
                                                        inv_vals.update({'x_studio_branch': bran})    

                                                    if self.inv_no_type == 'as_per_sheet':
                                                        inv_vals.update(
                                                            {"name": rowinv[4]})

                                                    created_inv = False
                                                    if self.invoice_type == 'inv':
                                                        inv_vals.update(
                                                            {"move_type": "out_invoice"})
                                                        searchinv = self.env['account.move'].search([('name', '=', rowinv[4])], limit=1)
                                                        if searchinv:
                                                            continue
                                                        else:
                                                            created_inv = inv_obj.with_context(
                                                            default_move_type='out_invoice').create(inv_vals)
                                                    elif self.invoice_type == 'bill':
                                                        inv_vals.update(
                                                            {"move_type": "in_invoice"})
                                                        created_inv = inv_obj.with_context(
                                                            default_move_type='in_invoice').create(inv_vals)
                                                    elif self.invoice_type == 'ccn':
                                                        inv_vals.update(
                                                            {"move_type": "out_refund"})
                                                        created_inv = inv_obj.with_context(
                                                            default_move_type='out_refund').create(inv_vals)
                                                    elif self.invoice_type == 'vcn':
                                                        inv_vals.update(
                                                            {"move_type": "in_refund"})
                                                        created_inv = inv_obj.with_context(
                                                            default_move_type='in_refund').create(inv_vals)

                                                    invoice_line_ids = []
                                                    created_inv_list_for_validate.append(
                                                        created_inv.id)
                                                    created_inv_list.append(created_inv.id)

                                                if created_inv:                                        
                                                    logger.error("Invoice Created : " + str(rowinv[4]))

                                                    field_nm = 'name'
                                                    if self.product_by == 'name':
                                                        field_nm = 'id'
                                                    elif self.product_by == 'int_ref':
                                                        field_nm = 'id'
                                                    elif self.product_by == 'barcode':
                                                        field_nm = 'id'

                                                    search_product = self.env['product.product'].search(
                                                        [('product_tmpl_id', '=', int(item_odoo[0]))], limit=1)
                                                        
                                                    if search_product:
                                                        vals.update(
                                                            {'product_id': search_product.id})

                                                        #if sheet.cell(row, 4).value != '':
                                                        #    vals.update(
                                                        #        {'name': sheet.cell(row, 4).value})
                                                        #else:
                                                        product = None
                                                        name = ''
                                                        if created_inv.partner_id:
                                                            if created_inv.partner_id.lang:
                                                                product = search_product.with_context(
                                                                    lang=created_inv.partner_id.lang)
                                                            else:
                                                                product = search_product

                                                            name = product.partner_ref
                                                        if created_inv.move_type in ('in_invoice', 'in_refund') and product:
                                                            if product.description_purchase:
                                                                name += '\n' + product.description_purchase
                                                        elif product:
                                                            if product.description_sale:
                                                                name += '\n' + product.description_sale
                                                        vals.update({'name': name})

                                                        accounts = search_product.product_tmpl_id.get_product_accounts(
                                                            created_inv.fiscal_position_id)
                                                        account = False
                                                        if created_inv.move_type in ('out_invoice', 'out_refund'):
                                                            account = accounts['income']
                                                        else:
                                                            account = accounts['expense']

                                                        if not account:
                                                            skipped_line_no[str(
                                                                counter)] = " - Account not found. "
                                                            counter = counter + 1
                                                            if created_inv.id in created_inv_list_for_validate:
                                                                created_inv_list_for_validate.remove(
                                                                    created_inv.id)
                                                            continue
                                                        else:
                                                            vals.update(
                                                                {'account_id': account.id})

                                                        if row[5] != '':
                                                            vals.update(
                                                                {'quantity': row[5]})
                                                        else:
                                                            vals.update({'quantity': 1})

                                                        if row[13] != '0':
                                                            vals.update(
                                                                {'discount': row[13]})
                                                        
                                                        punit = "Units"
                                                        if punit in (None, ""):
                                                            if created_inv.move_type in ('in_invoice', 'in_refund') and search_product.uom_po_id:
                                                                vals.update(
                                                                    {'product_uom_id': search_product.uom_po_id.id})
                                                            elif search_product.uom_id:
                                                                vals.update(
                                                                    {'product_uom_id': search_product.uom_id.id})
                                                        else:
                                                            search_uom = self.env['uom.uom'].search(
                                                                [('name', '=', punit)], limit=1)
                                                            if search_uom:
                                                                vals.update(
                                                                    {'product_uom_id': search_uom.id})
                                                            else:
                                                                skipped_line_no[str(
                                                                    counter)] = " - Unit of Measure not found. "
                                                                counter = counter + 1
                                                                if created_inv.id in created_inv_list_for_validate:
                                                                    created_inv_list_for_validate.remove(
                                                                        created_inv.id)
                                                                continue

                                                        if row[11] in (None, ""):
                                                            if created_inv.move_type in ('in_invoice', 'in_refund'):
                                                                vals.update(
                                                                    {'price_unit': search_product.standard_price})
                                                            else:
                                                                vals.update(
                                                                    {'price_unit': search_product.lst_price})
                                                        else:
                                                            vals.update(
                                                                {'price_unit': row[11]})
                                                            
                                                        tatx = "Sales Tax 5%"    
                                                        if tatx in (None, ""):
                                                            if created_inv.move_type in ('in_invoice', 'in_refund') and search_product.supplier_taxes_id:
                                                                vals.update(
                                                                    {'tax_ids': [(6, 0, search_product.supplier_taxes_id.ids)]})
                                                            elif created_inv.move_type in ('out_invoice', 'out_refund') and search_product.taxes_id:
                                                                vals.update(
                                                                    {'tax_ids': [(6, 0, search_product.taxes_id.ids)]})

                                                        else:
                                                            taxes_list = []
                                                            some_taxes_not_found = False
                                                            for x in tatx.split(','):
                                                                x = x.strip()
                                                                if x != '':
                                                                    search_tax = self.env['account.tax'].search(
                                                                        [('name', '=', x)], limit=1)
                                                                    if search_tax:
                                                                        taxes_list.append(
                                                                            search_tax.id)
                                                                    else:
                                                                        some_taxes_not_found = True
                                                                        skipped_line_no[str(
                                                                            counter)] = " - Taxes " + x + " not found. "
                                                                        break
                                                            if some_taxes_not_found:
                                                                counter = counter + 1
                                                                if created_inv.id in created_inv_list_for_validate:
                                                                    created_inv_list_for_validate.remove(
                                                                        created_inv.id)
                                                                continue
                                                            else:
                                                                vals.update(
                                                                    {'tax_ids': [(6, 0, taxes_list)]})

                                                        vals.update(
                                                            {'move_id': created_inv.id})
                                                        invoice_line_ids.append((0, 0, vals))
                                                        vals = {}

                                                        counter = counter + 1

                                                    else:
                                                        skipped_line_no[str(
                                                            counter)] = " - Product not found. "
                                                        counter = counter + 1
                                                        if created_inv.id in created_inv_list_for_validate:
                                                            created_inv_list_for_validate.remove(
                                                                created_inv.id)
                                                        continue
                                                    created_inv.write(
                                                        {'invoice_line_ids': invoice_line_ids})
                                                    invoice_line_ids = []
                                                else:
                                                    logger.error("Invoice not created : " + str(rowinv[4]) )

                                                    skipped_line_no[str(
                                                        counter)] = " - Order not created. "
                                                    counter = counter + 1
                                                    continue

                                            else:
                                                skipped_line_no[str(
                                                    counter)] = " - Number or Product field is empty. "
                                                counter = counter + 1

                                        except Exception as e:
                                            skipped_line_no[str(
                                                counter)] = " - Value is not valid " + ustr(e)
                                            counter = counter + 1
                                            continue
                                invoices = inv_obj.search( [('id', 'in', created_inv_list)])
                                if invoices:
                                    for invoice in invoices:
                                        invoice._onchange_partner_id()
                                        invoice._onchange_quick_edit_line_ids()
                                        invoice.action_post()   
                                created_inv_list = []
                                self.env.cr.commit()

                            else:
                                break
                    #cursorsales.execute("SELECT * from sales_invoices LIMIT 5000")
                    #invoice_data =  cursorsales.fetchall()
                    #for numinv, rowinv in enumerate(invoice_data):
                except Exception as e:
                    raise UserError(
                        _("Sorry, Your excel file does not match with our format" + ustr(e) + " - " + traceback.format_exc()))

                if counter > 1:
                    completed_records = len(created_inv_list)
                    validate_rec = len(created_inv_list_for_validate)
                    res = self.show_success_msg(
                        completed_records, validate_rec, skipped_line_no)
                    return res
