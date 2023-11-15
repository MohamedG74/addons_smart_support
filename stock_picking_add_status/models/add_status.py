from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from decimal import *
from datetime import datetime
from io import BytesIO
import base64
from xlrd import open_workbook, xldate_as_datetime
from io import StringIO 
import json



class add_button(models.Model):
    _inherit = 'stock.picking'

    counts=fields.Char(string="counts of lines")

    stage=fields.Selection([('x_1','لم يتم الاستلام'),
                            ('x_2','إستلام جزئي'),
                            ('x_3','تم الاستلام'),], string="حالة استلام العميل", default='x_1', store=True, readonly=True, compute='_compute_stage')
    
    driver_state=fields.Selection([('x_4','لم يتم الاستلام من السائق'),
                                   ('x_5','تم الاستلام من السائق'),] ,default='x_4', string="حالة استلام السائق")
    
    #this is the user who create the transfer
    user_create_id = fields.Many2one('res.users', string='User')
    user_create_name = fields.Char(string='Created User')

    #this is the user who validate the transfer
    user_id = fields.Many2one('res.users', string='User')
    user_name = fields.Char(string='Validated User')

    #this is the user who create the transfer
    first_user = fields.Many2one(related='message_follower_ids.partner_id', string='First User', limit=1)






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

            stock_move_values = []
            for row_idx in range(1, wb_sheet.nrows):
                default_code = wb_sheet.cell(row_idx, 0).value
                # product_name = wb_sheet.cell(row_idx, 1).value
                # name = wb_sheet.cell(row_idx, 2).value
                product_uom_qty = wb_sheet.cell(row_idx, 1).value


                # Check if default_code is numeric and convert it to a string
                if isinstance(default_code, (int, float)):
                    default_code = str(float(default_code))
                else:
                    default_code = str(default_code)


                # Look up the product by name
                product = self.env['product.product'].search([('default_code', '=', default_code)])

                if product:
                    stock_move_values.append({
                        "default_code": default_code,
                        "product_id": product.id,
                        "location_id": self.location_id.id,  # Set the location_id to 8
                        "location_dest_id": self.location_dest_id.id,  # Set the location_dest_id to 5,
                        "name": product.display_name,
                        "product_uom_qty": product_uom_qty,
                    })
                    # print(f"default_code: {default_code},")
                else:
                    raise ValueError(f"Product with Default Code '{default_code}' not found.")

            # if stock_move_values:
            #     x= self.env['stock.move'].create(stock_move_values)
            #     self.env.cr.commit()
            # print(f"Stock Move Values: {x}")

            if stock_move_values:
                stock_move_records = self.env['stock.move'].create(stock_move_values)
                for stock_move_record in stock_move_records:
                    # Assuming move_ids_without_package is a One2many field
                    self.move_ids_without_package = [(0, 0, {
                        'product_id': stock_move_record.product_id.id,
                        "default_code": stock_move_record.default_code,
                        "location_id": stock_move_record.location_id.id,
                        "location_dest_id": stock_move_record.location_dest_id.id,
                        "name": stock_move_record.name,
                        "product_uom_qty": stock_move_record.product_uom_qty,
                    })]

                # Commit the changes
                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(u'ERROR: {}'.format(e))
                





    # @api.depends('move_ids.actually_received', 'move_ids.quantity_done', 'move_ids.reminder')
    # def _compute_stage(self):
    #     for rec in self:
    #         if rec.move_ids.actually_received == rec.move_ids.quantity_done:
    #             rec.stage = 'x_3'
    #         elif rec.move_ids.actually_received == 0:
    #             rec.stage = 'x_1'
    #         elif rec.move_ids.actually_received <  rec.move_ids.quantity_done or rec.move_ids.reminder != 0:
    #             rec.stage = 'x_2'

    @api.depends('move_ids.actually_received', 'move_ids.quantity_done', 'move_ids.reminder')
    def _compute_stage(self):
        for rec in self:
            if not rec.move_ids:
                rec.stage = 'x_1'
            else:
                # moves = rec.move_ids
                # if all(move.actually_received == move.quantity_done and move.quantity_done !=0 for move in moves):
                #     rec.stage = 'x_3'
                # elif any(move.actually_received == 0 and move.reminder != 0 for move in moves):
                #     rec.stage = 'x_1'
                # elif any(move.actually_received < move.quantity_done and move.reminder != 0 for move in moves):
                #     rec.stage = 'x_2'
                moves = rec.move_ids
                total_actually_received = sum(move.actually_received for move in moves)
                total_quantity_done = sum(move.quantity_done for move in moves)

                if total_actually_received == total_quantity_done and total_quantity_done != 0:
                    rec.stage = 'x_3'
                elif total_actually_received == 0:
                    rec.stage = 'x_1'
                elif total_actually_received < total_quantity_done:
                    rec.stage = 'x_2'


    def action_in_way(self):
        for rec in self:
            rec.driver_state= "x_5"
    
    
    def action_pass_value(self):
        for rec in self:
            # current_user = self.env.user
            for move in rec.move_ids:
                move.actually_received = move.quantity_done
                move._onchange_actually_received()    


    @api.model_create_multi
    def create(self, vals_list):
        res = super(add_button, self).create(vals_list)

        # Add your code here to save the user's ID and name
        current_user = self.env.user
        for sequence in res:
            sequence.write({
                'user_create_id': current_user.id,
                'user_create_name': current_user.name,
            })
        return res
        

    def button_validate(self):
        res = super(add_button, self).button_validate()

        # Add your code here to save the user's ID and name
        current_user = self.env.user
        self.write({
            'user_id': current_user.id,
            'user_name': current_user.name,
        })
        return res





    # @api.depends('move_ids_without_package')
    # def _compute_last_line_count(self):
    #     for record in self:
    #         record.counts = len(record.move_ids_without_package)

    # @api.depends('move_ids_without_package')
    # @api.model_create_multi
    # def create(self,vals):
    #     for record in vals:
    #         record['counts']= str(len(self.move_ids_without_package))
    #     return super(add_button, self).create(vals)
    
    # @api.constrains('move_ids_without_package') 
    # def check_move_ids_without_package(self):
    #     if self.origin:
    #         if len(self.move_ids_without_package) > self.counts :
    #             raise ValidationError(('Warning! You cannot add multiple lines.'))


    

class default_code_stock(models.Model):

    _inherit = 'stock.move'
    default_code = fields.Char(string="Internal Reference",related='product_id.default_code')

    actually_received=fields.Float(string="المستلم فعلياً")
    reminder=fields.Float(string="المتبقي")

    @api.onchange('actually_received')
    def _onchange_actually_received(self):
            self.reminder = Decimal((self.quantity_done - self.actually_received)).quantize(Decimal('.0001'))
    




class stock_picking_kanban(models.Model):
    _inherit = 'stock.picking.type'

    count_none = fields.Integer(compute='_compute_stage_count_none')
    count_partially = fields.Integer(compute='_compute_stage_count_partially')

    def _compute_stage_count_none(self):
        for rec in self:
            rec.count_none = self.env['stock.picking'].search_count([('stage', '=', 'x_1'),('picking_type_id', '=', rec.ids)])

    def _compute_stage_count_partially(self):
        for rec in self:
            rec.count_partially = self.env['stock.picking'].search_count([('stage', '=', 'x_2'),('picking_type_id', '=', rec.ids)])

    
    def get_action_none_stage(self):
        return self._get_action('stock_picking_add_status.action_none_stage')
    
    def get_action_partially_stage(self):
        return self._get_action('stock_picking_add_status.action_partially_stage')