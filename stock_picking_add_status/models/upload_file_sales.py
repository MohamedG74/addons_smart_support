from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from decimal import *
from datetime import datetime
from io import BytesIO
import base64
from xlrd import open_workbook, xldate_as_datetime
from io import StringIO 
import json

class default_code_sales(models.Model):
    _inherit = 'sale.order.line'
    
    default_code = fields.Char(string="Internal Reference",related='product_id.default_code')



class upload_file_sales(models.Model):
    _inherit = 'sale.order'


    #load data from excel file
    upload_file = fields.Binary(string='Upload file')
    document_name=fields.Char(string="Document Name")

    def action_upload(self):
        if not self.upload_file:
            raise ValidationError(_('Please upload your file'))
        try:
            inputx = BytesIO()
            inputx.write(base64.decodebytes(self.upload_file))
            book = open_workbook(file_contents=inputx.getvalue())
            wb_sheet = book.sheet_by_index(0)

            sale_order_lines = []
            for row_idx in range(1, wb_sheet.nrows):
                default_code = wb_sheet.cell(row_idx, 0).value
                # product_name = wb_sheet.cell(row_idx, 1).value
                # name = wb_sheet.cell(row_idx, 2).value
                product_uom_qty = wb_sheet.cell(row_idx, 1).value
                # product_uom = wb_sheet.cell(row_idx, 2).value

                # Look up the product by name
                product = self.env['product.product'].search([('default_code', '=', default_code)])

                # Look up the product_uom by name
                # product_uom = self.env['uom.uom'].search([('name', '=', product_uom)])

                if product:
                    # if product_uom:
                    sale_order_lines.append({
                        "default_code": default_code,
                        "product_id": product.id,
                        "name": product.display_name,
                        "product_uom_qty": product_uom_qty,
                        # "product_uom": product_uom,
                        "order_id": self.id,
                    })
                    print(f"default_code: {default_code}")
                    # else:
                    #     raise ValueError(f"Product UOM '{product_uom}' not found.")
                else:
                    raise ValueError(f"Product with Default Code '{default_code}' not found.")

            if sale_order_lines:
                sale_order_records = self.env['sale.order.line'].create(sale_order_lines)
                # for sale_order_record in sale_order_records:
                #     # Assuming order_line is a One2many field
                #     self.order_line = [(0, 0, {
                #         'product_id': sale_order_record.product_id.id,
                #         "default_code": sale_order_record.default_code,
                #         "name": sale_order_record.name,
                #         "product_uom_qty": sale_order_record.product_uom_qty,
                #         # "product_uom": sale_order_record.product_id.product_uom.id,
                #     })]

                # Commit the changes
                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(u'ERROR: {}'.format(e))