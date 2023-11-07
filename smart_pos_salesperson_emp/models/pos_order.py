# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo import http
from odoo.http import request
import json


class PosOrderLine(models.Model):
    _inherit = 'pos.order.line'

    user_id = fields.Many2one('hr.employee', string='Salesperson')

class PosOrder(models.Model):
    _inherit = 'pos.order'

    user_id_custom = fields.Many2one('hr.employee', string='Salesperson')

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_commissionable=fields.Boolean('Is Commissionable')

class ProductProduct(models.Model):
    _inherit = "product.product"

    is_commissionable=fields.Boolean('Is Commissionable')

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_product_product(self):
        result = super()._loader_params_product_product()
        result['search_params']['fields'].append('is_commissionable')
        return result
#product.product

class Employe(models.Model):
    _inherit = 'hr.employee'
    @api.model
    def get_employee_sales_data(self):
        employees = self.search([('department_id','=',3)])  # fetch all HR employees
        employee_data = []
        for employee in employees:
            employee_data.append({
                'id': employee.id,
                'name': employee.name,
                'user_id': employee.user_id.id,
                # add more fields as needed
            })
        return employee_data

class PosController(http.Controller):

    @http.route('/pos/employee_data', type='json', auth='none')
    def get_employee_sales_data(self):
        employees = request.env['hr.employee'].get_employee_sales_data()
        return json.dumps(employees)