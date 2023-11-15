from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from decimal import *
from datetime import datetime
from io import BytesIO
import base64
from xlrd import open_workbook, xldate_as_datetime
from io import StringIO 
import json

class default_code_purchase(models.Model):

    _inherit = 'purchase.order.line'
    default_code = fields.Char(string="Internal Reference",related='product_id.default_code')



class upload_file_purchase(models.Model):
    _inherit = 'purchase.order'


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

            purchase_order_lines = []
            for row_idx in range(1, wb_sheet.nrows):
                default_code = wb_sheet.cell(row_idx, 0).value
                # product_name = wb_sheet.cell(row_idx, 1).value
                # name = wb_sheet.cell(row_idx, 2).value
                product_qty = wb_sheet.cell(row_idx, 1).value
                price_unit = wb_sheet.cell(row_idx, 2).value

                # Look up the product by name
                product = self.env['product.product'].search([('default_code', '=', default_code)])

                if product:
                    purchase_order_lines.append({
                        "default_code": default_code,
                        "product_id": product.id,
                        "name": product.display_name,
                        "product_qty": product_qty,
                        "price_unit": price_unit,
                        "order_id": self.id,
                    })
                    print(f"default_code: {default_code},")
                else:
                    raise ValueError(f"Product with Default Code '{default_code}' not found.")

            if purchase_order_lines:
                purchase_order_records = self.env['purchase.order.line'].create(purchase_order_lines)
                # for purchase_order_record in purchase_order_records:
                #     # Assuming order_line is a One2many field
                #     self.order_line = [(0, 0, {
                #         'product_id': purchase_order_record.product_id.id,
                #         "default_code": purchase_order_record.default_code,
                #         "name": purchase_order_record.name,
                #         "product_qty": purchase_order_record.product_qty,
                #         "price_unit": purchase_order_record.price_unit,
                #     })]

                # Commit the changes
                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(u'ERROR: {}'.format(e))