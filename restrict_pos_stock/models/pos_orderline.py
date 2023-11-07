# -*- coding: utf-8 -*-

import datetime
from odoo import http,fields, models,api
import requests as reqtwo
import json
from odoo.exceptions import UserError,  AccessError, MissingError
from odoo.addons.account.controllers.portal import PortalAccount
from odoo.http import request

class POSOrderLine(models.Model):
    _inherit = 'pos.order.line'

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
        return super(POSOrderLine, self.sudo()).search_read(domain, fields, offset, limit, order)

    secondary_qty = fields.Float("Secondary Unit Qty")
    secondary_uom_id = fields.Many2one('uom.uom', string="Secondary Unit")

class PosOrder(models.Model):
    _inherit = 'pos.order'

    to_invoice = fields.Boolean(default=True)
    to_ship = fields.Boolean(default=False)

    def create(self, vals):
        vals['to_invoice'] = True
        vals['to_ship'] = False
        #vals['account_movename'] = self.env["account.move"].search([("id","=",vals['account_move'].id)],limit=1).name
        return super(PosOrder, self).create(vals)
    
    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None):
         return super(PosOrder, self.sudo()).search_read(domain, fields, offset, limit, order)

    @api.model
    def search_read(self, domain=None, fields=None, offset=0, limit=None, order=None,load=None):
        if(load != None):
            return super(PosOrder, self.sudo()).search_read(domain, fields, offset, limit, order)
        else:
            return super(PosOrder, self.sudo()).search_read(domain, fields, offset, limit, order)


    order_note = fields.Char('Order Note')
    account_movename = fields.Char('INV Number')
    account_movetype = fields.Char('Move Type')
    account_movedelivery = fields.Char('Move Type')

    def _order_fields(self, ui_order):
        res = super(PosOrder, self)._order_fields(ui_order)
        res['order_note'] = ui_order.get('order_note', False)
        res['user_id_custom'] = ui_order.get('user_id_custom', False)
        res['account_movename'] = ui_order.get('account_movename', False)
        res['account_movetype'] = ui_order.get('account_movetype', False)
        res['account_movedelivery'] = ui_order.get('account_movedelivery', False)
        return res

    def _export_for_ui(self, order):
        res = super()._export_for_ui(order)
        res['order_note'] = order.order_note,
        res['user_id_custom'] = order.user_id_custom.id
        res['account_movename'] = order.account_move.name
        res['account_movetype'] = order.account_move.move_type
        res['account_movedelivery'] = order.account_move.delivery_status
        return res
    
class newPortal(PortalAccount):
    @http.route(['/my/invoices/<int:invoice_id>'], type='http', auth="public", website=True)
    def portal_my_invoice_detail(self, invoice_id, access_token=None, report_type=None, download=False, **kw):
        invoice_sudo = request.env["account.move"].browse([invoice_id]).sudo()

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=invoice_sudo, report_type=report_type, report_ref='account.report_whats', download=download)

        values = self._invoice_get_page_view_values(invoice_sudo, access_token, **kw)
        return request.render("account.portal_invoice_page", values)

    
class AccountMove(models.Model):
    _inherit = ['account.move']
    
    sent_whatsapp = fields.Boolean(string="Whatsapp Sent Indicator",default=False)

    @api.model
    def create(self, vals):
        if(vals.get('ref')):
            get_order = self.env['pos.order'].search([('name','=',vals.get('ref'))],limit=1)
            if(get_order):
                if(get_order.user_id_custom):
                    vals['x_studio_employee'] = get_order.user_id_custom.id
                if(get_order.order_note):
                    vals['x_studio_notes'] = get_order.order_note
                #get session and config
                if(get_order.session_id):
                    pos_config = self.env['pos.session'].search([('id','=',get_order.session_id.id)],limit=1)
                    if(pos_config.config_id):
                        pos_conf = self.env['pos.config'].search([('id','=',pos_config.config_id.id)],limit=1)
                        if(pos_conf.operating_unit_id):
                            vals['x_studio_branch'] = pos_conf.operating_unit_id.id

        return super(AccountMove, self).create(vals)

    def send_whatsapp(self):
        for rec in self:
            if(rec.partner_id.country_id.id == 65):
                phone = '2' + str(rec.partner_id.mobile)
            else:
                phone = '966' + str(rec.partner_id.mobile)
            url = "https://waba.360dialog.io/v1/messages"
            downloadlink = 'https://erp.meshkati.sa/my/invoices/%s?access_token=%s&report_type=pdf&download=true' % (rec.id, rec._portal_ensure_token())
            payload = json.dumps({
            "to": phone,
            "type": "template",
            "template": {
                "namespace": "d2ff8e13_413a_4a0e_a0a6_20af3187e5fb",
                "language": {
                "policy": "deterministic",
                "code": "AR"
                },
                "name": "pos_invoice",
                "components": [
                {
                    "type": "header",
                    "parameters": [
                    {
                        "type": "document",
                        "document": {
                        "filename": "Invoice-%s.pdf" % (rec.name),
                        "link": downloadlink
                        }
                    }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                    {
                        "type": "text",
                        "text": "INV-%s" % (rec.name)
                    }
                    ]
                }
                ]
            }
            })
            headers = {
            'D360-API-KEY': 'cjOCXqLiM5dJhmXuuV2WnMofAK',
            'Content-Type': 'application/json'
            }
            response = reqtwo.request("POST", url, headers=headers, data=payload)
            rec.write({'sent_whatsapp':True})
            #raise UserError("Sent to " + phone + ": " + downloadlink)

    @api.model
    def send_whatsapp_for_last_minute_records(self):
        last_minute = datetime.datetime.now() - datetime.timedelta(minutes=5)
        records = self.env['account.move'].search([('create_date', '>', last_minute),('sent_whatsapp','=', False)])
        for record in records:
            record.send_whatsapp()
