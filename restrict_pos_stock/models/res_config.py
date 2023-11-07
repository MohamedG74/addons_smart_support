from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_is_zero


class PosConfig(models.Model):
    _inherit = 'pos.config'
    smart_without_stock = fields.Boolean("Allow Selling Without Stock")
    select_uom_type = fields.Selection([('primary', 'Primary'), (
        'secondary', 'Secondary')], string='Select Default UOM type', default='primary')
    display_uom_in_receipt = fields.Boolean(string='Display UOM in Receipt')
    enable_price_to_display = fields.Boolean(
        string='Display price in Secondary UOM ?')
    
    #pos note
    enable_orderline_note = fields.Boolean(
        "Enable OrderLine Note", default=False)
    enable_order_note = fields.Boolean(
        "Enable Global Note", default=True)
    display_orderline_note_receipt = fields.Boolean(
        "Display Line Note in Receipt", default=False)
    display_order_note_receipt = fields.Boolean(
        "Display Global Note in Receipt", default=True)
    display_order_note_payment = fields.Boolean(
        "Display Global Note in Payment", default=True)
    hide_extra_note_checkbox = fields.Boolean(string = "Hide Store Extra Note")

    operating_unit_id = fields.Many2one('operating.unit',string = "POS Branch")

    # admin_user = fields.Many2one('res.users',string = "Admin User")
        
    return_journal_id = fields.Many2one(
        'account.journal', string='Invoice Journal',
        domain=[('type', '=', 'sale')],
        help="Accounting journal used to create invoices.")


class posConfigInherit(models.TransientModel):
    _inherit = 'res.config.settings'
    operating_unit_id = fields.Many2one(
        related="pos_config_id.operating_unit_id", readonly=False)
    
    # admin_user = fields.Many2one(
    #     related="pos_config_id.admin_user", readonly=False)
    
    smart_without_stock = fields.Boolean(
        related="pos_config_id.smart_without_stock", readonly=False)

    pos_display_uom_in_receipt = fields.Boolean(
        related="pos_config_id.display_uom_in_receipt", readonly=False)
    pos_enable_price_to_display = fields.Boolean(
        related="pos_config_id.enable_price_to_display", readonly=False)
    pos_select_uom_type = fields.Selection(
        related="pos_config_id.select_uom_type", readonly=False)
    
    pos_enable_orderline_note = fields.Boolean(related="pos_config_id.enable_orderline_note", readonly=False)
    pos_enable_order_note = fields.Boolean(related="pos_config_id.enable_order_note", readonly=False)
    pos_display_orderline_note_receipt = fields.Boolean(related="pos_config_id.display_orderline_note_receipt", readonly=False)
    pos_display_order_note_receipt = fields.Boolean(related="pos_config_id.display_order_note_receipt", readonly=False)
    pos_display_order_note_payment = fields.Boolean(related="pos_config_id.display_order_note_payment", readonly=False)
    pos_hide_extra_note_checkbox = fields.Boolean(related="pos_config_id.hide_extra_note_checkbox", readonly=False)

    pos_return_journal_id = fields.Many2one(related='pos_config_id.return_journal_id', readonly=False)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name'])
        return [(template.id, '%s' % (template.name))
                for template in self]

class ProductProduct(models.Model):
    _inherit = 'product.product'

    def name_get(self):
        # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
        self.browse(self.ids).read(['name'])
        return [(template.id, '%s' % (template.name))
                for template in self]
