# Part of Softhealer Technologies.
{
    "name": "Point of Sale Retail Shop| POS Retail Shop| All In One POS Retail| POS All In One| Point of sales All In One| POS Responsive| POS Order History| POS Order List| POS Bundle| POS Signature| POS Keyboard Shortcut| POS Direct Login",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "category": "Point of Sale",
    "summary": "cash in cash out own customer discount mass update product tags own product template auto validate pos quick print receipt import pos secondary product suggestion pos access right pos auto lock cancel whatsapp return exchange pos all feature Restaurant & Shop Retail All In One POS Enterprise POS Community All In One POS all in one features pos Reorder pos Reprint pos Coupon Discount pos Order Return pos order all pos all features pos discount pos order list print pos receipt pos item count retail pos retail import sale from pos create quote from pos odoo All in one pos Reprint pos Return POS Stock pos gift import sale from pos pos multi currency payment pos pay later pos internal transfer pos disable payment pos product template pos product operation pos loyalty rewards all pos reports pos stock pos retail pos label pos cash control pos cash in out pos cash out pos logo pos receipt all pos in one all pos in one retail  odoo",
    "description": """ This is the fully retail solution for any kind of retail shop or bussiness.  """,
    "version": "16.0.2",
    "depends": ["point_of_sale", 'utm', "portal", "pos_hr", "purchase"],
    "application": True,
    "license": "OPL-1",
    "data": [
        # Responsive theme
        'security/ir.model.access.csv',
        'data/sh_pos_theme_responsive/pos_theme_settings_data.xml',
        'sh_pos_theme_responsive/views/pos_config_view.xml',
        'views/res_pos_config.xml',

        # Product Suggesion
        'pos_product_suggestion/views/product_view.xml',
        
        # Base bundole
        'sh_base_bundle/views/sh_product_view.xml',

        # Access Rights
        'security/sh_pos_access_rights_groups.xml',

        # Pos Cancel 
        'sh_pos_cancel/security/pos_cancel_feature.xml',
        'sh_pos_cancel/data/server_action_data.xml',
        'sh_pos_cancel/views/pos_order_views.xml',

        # Pos Chatter
        'sh_pos_chatter/security/sh_pos_chatter_groups.xml',
        'sh_pos_chatter/views/pos_order_views.xml',

        # Keyboard Shortcut
        'sh_pos_keyboard_shortcut/data/sh_keyboard_key_data.xml',
        'views/pos_config.xml',

        # Multi barcode
        'sh_product_multi_barcode/views/product_view.xml',
        'sh_product_multi_barcode/views/res_config_settings.xml',

        # Return Exchange
        'sh_pos_order_return_exchange/views/product_template.xml',

        # pos order disocunt
        'sh_pos_discount/views/pos_discount.xml',
        'sh_pos_discount/views/pos_order.xml',

        'sh_pos_customer_discount/views/res_partner_views.xml',

        # pos note
        'sh_pos_note/views/pos_order.xml',
        'sh_pos_note/views/pre_define_note.xml',

        # order signature
        'sh_pos_order_signature/views/pos_order_view.xml',

        # own customer
        'sh_pos_own_customers/views/res_partner.xml',

        # own product
        'sh_pos_own_products/views/product.xml',

        'sh_product_tags/wizard/mass_tag_update_wizard_view.xml',

        # order label
        'sh_pos_order_label/data/demo_product.xml',
        'sh_pos_order_label/views/pos_order.xml',

        # pos weight
        'sh_pos_weight/views/pos_order.xml',

        'sh_message/wizard/sh_message_wizard.xml',
        
        # qty pack
        'sh_pos_product_qty_pack/views/product.xml',

        # base uom qty pack
        'sh_base_uom_qty_pack/views/product_product_views.xml',
        'sh_base_uom_qty_pack/views/product_template_views.xml',

        # profict report
        'security/import_pos_groups.xml',
        'sh_pos_profit/report/report_pos_sales_details_templates.xml',
        'sh_import_pos/wizard/import_pos_wizard_views.xml',
        'sh_import_pos/views/pos_views.xml',


        # category merge
        'sh_pos_categories_merge/views/view.xml',
        'sh_pos_categories_merge/wizard/merge_category_wizard.xml',

        'sh_pos_product_template/views/pos_template_product.xml',

        # base secondary uom
        'sh_product_secondary/views/product_product_views.xml',
        'sh_product_secondary/views/product_template_views.xml',
        'sh_product_secondary/views/stock_quant_views.xml',

        # pos secondary 
        'sh_pos_secondary/views/pos_order.xml',

        # cash in out
        'sh_pos_cash_in_out/views/cash_in_out_menu.xml',

        'security/sh_product_tags_groups.xml',
        'sh_product_tags/views/product_tags_views.xml',
        'sh_product_tags/views/product_views.xml',
        'sh_product_tags/views/res_config_settings_views.xml',

        # Whatsapp integration
        'sh_pos_whatsapp_integration/views/res_users.xml',

        'sh_pos_rounding/data/data.xml',

        # Pos Receipt
        'security/sh_pos_receipt_groups.xml',
        'sh_pos_receipt/report/pos_order_reports.xml',
        'data/mail_template_data.xml',
        'sh_pos_receipt/report/pos_order_templates.xml',
        'sh_pos_receipt/views/pos_order_views.xml',

        'sh_portal_pos/views/pos_order_templates.xml',
        

        'sh_pos_line_pricelist/views/res_config_settings.xml',

        
        'sh_pos_direct_login/views/res_users.xml',

        'data/cron_view.xml',
        'sh_auto_validate_pos/views/log_track_view.xml',


        # Multiples qty
        'sh_pos_multiples_qty/views/product.xml',

        'sh_pos_min_qty/views/res_config_settings.xml',

        # variant
        'sh_pos_product_variant/views/product_template.xml',

        'sh_pos_customer_maximum_discount/views/res_partner_views.xml',

    ],
    'assets': {
        'point_of_sale.assets': [
            "/sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/scss/pos_theme_variables.scss",
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/scss/fonts.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/scss/pos_theme.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/css/*',
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/js/**/*',
            'sh_pos_all_in_one_retail/static/sh_pos_theme_responsive/static/src/xml/**/*',

            # Product Suggestion
            'sh_pos_all_in_one_retail/static/pos_product_suggestion/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/pos_product_suggestion/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/pos_product_suggestion/static/src/js/products_widget.js',
            'sh_pos_all_in_one_retail/static/pos_product_suggestion/static/src/xml/products_widget.xml',

            # Product Bundle
            'sh_pos_all_in_one_retail/static/sh_pos_product_bundle/static/src/js/**/*',
            'sh_pos_all_in_one_retail/static/sh_pos_product_bundle/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_product_bundle/static/src/xml/**/*',

            # Access Rights
            'sh_pos_all_in_one_retail/static/sh_pos_access_rights/static/src/js/**/*',
            'sh_pos_all_in_one_retail/static/sh_pos_access_rights/static/src/scss/pos.scss',

            # POS Auto lock
            'sh_pos_all_in_one_retail/static/sh_pos_auto_lock/static/src/js/Chrome.js',
            'sh_pos_all_in_one_retail/static/sh_pos_auto_lock/static/src/scss/pos.scss',

            # Bag Charges
            'sh_pos_all_in_one_retail/static/sh_pos_bag_charges/static/src/js/BagCategory_list_popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_bag_charges/static/src/js/BagChargesBtn.js',
            'sh_pos_all_in_one_retail/static/sh_pos_bag_charges/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_bag_charges/static/src/xml/bag_charges.xml',

            # Pos Counter
            'sh_pos_all_in_one_retail/static/sh_pos_counter/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_counter/static/src/js/counter.js',
            'sh_pos_all_in_one_retail/static/sh_pos_counter/static/src/xml/order_receipt.xml',

            # Default Customer
            'sh_pos_all_in_one_retail/static/sh_pos_default_customer/static/src/js/pos.js',

            # default invoice
            'sh_pos_all_in_one_retail/static/sh_pos_default_invoice/static/src/js/Screens/payment_screen.js',

            # Keyboard Shortcut
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/js/Popups/ShortcutTipsPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/js/Screens/ProductScreen/ControlButtons/ShortcutListTips.js',
            'sh_pos_all_in_one_retail/static/sh_pos_keyboard_shortcut/static/src/xml/**/*',

            # pos Multi barcode
            'sh_pos_all_in_one_retail/static/sh_pos_multi_barcode/static/src/js/DB.js',
            'sh_pos_all_in_one_retail/static/sh_pos_multi_barcode/static/src/js/Models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_multi_barcode/static/src/js/posWidget.js',

            # Pos Order list 
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/lib/jquery.simplePagination.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/js/ActionButtons/OrderHistoryButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/js/screens/OrderListScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/js/screens/PaymentScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/scss/simplePagination.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/xml/ActionButtons/OrderHistoryButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_list/static/src/xml/screens/OrderListScreen.xml',
            
            # Pos Order Return/Exchange 
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/js/Popups/ReturnOrderPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/js/screens/OrderListScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/js/screens/PaymentScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/js/Models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/xml/receipt.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/xml/ReturnOrderPopup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange/static/src/xml/screen.xml',

            # Receipt Extends
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/libs/jquery.qrcode.min.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/libs/JsBarcode.all.min.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/js/Screen/ReceiptScreen/AbstractReceiptScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/js/Screen/ReceiptScreen/receiptScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/js/Screen/TicketScreen/TicketScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_receipt_extend/static/src/xml/pos.xml',

            # Return Exchange Barcode
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/js/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/js/ReturnPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_return_exchange_barcode/static/src/xml/pos.xml',

            # POS Product Warehouse Qty
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/popups/ProductQtyPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/popups/QuantityWarningPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/Screens/PaymentScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/Screens/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/Screens/ProductsWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/js/Screens/TicketScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/xml/popups/ProductQtyPopup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/xml/popups/QuantityWarningPopup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/xml/screens/ProductItem.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock/static/src/xml/Orderline.xml',

            # Realtime Stock Update
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock_adv/static/src/js/screeen/PaymentScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock_adv/static/src/js/chrome.js',
            'sh_pos_all_in_one_retail/static/sh_pos_wh_stock_adv/static/src/js/models.js',

            # Remove Cart Item
            'sh_pos_all_in_one_retail/static/sh_pos_remove_cart_item/static/src/js/ControlButton/RemoveAllItemButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_remove_cart_item/static/src/scss/custom.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_remove_cart_item/static/src/xml/controlButtons/action_button.xml',

            # pos order discount
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/js/popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/js/screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/xml/Popup/DiscountPopupWidget.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/xml/Orderline.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_discount/static/src/xml/OrderLinesReceipt.xml',

            # pos order discount
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Popups/GlobalDiscountPopupWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Screens/ProductScreen/ControlButtons/GlobalDiscountButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Screens/ProductScreen/ControlButtons/RemoveDiscountButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Screens/ProductScreen/NumpadWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Screens/ProductScreen/OrderSummary.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/Screens/ProductScreen/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/xml/Popups/GlobalDiscountPopupWidget.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/xml/Screens/ProductScreen/ControlButtons/GlobalDiscountButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/xml/Screens/ProductScreen/ControlButtons/RemoveDiscountButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_discount/static/src/xml/Screens/ProductScreen/OrderSummary.xml',

            'sh_pos_all_in_one_retail/static/sh_pos_customer_discount/static/src/js/Screens/PartnerListScreen/PartnerListScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_discount/static/src/js/models.js',
            
            # pos Note
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/js/Popups/popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/js/Screens/screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/js/action_button.js',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/xml/Popups/popup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/xml/Screens/screen.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/xml/action_button.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/xml/orderline.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_note/static/src/xml/receipt.xml',

            # point of sale product creation
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/js/Popups/product_popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/js/product_button.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/xml/Popups/product_popup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_product_creation/static/src/xml/product_button.xml',

            # point of sale logo chnages
            'sh_pos_all_in_one_retail/static/sh_pos_logo/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_logo/static/src/xml/Screens/ReceiptScreeen/OrderReceipt.xml',

            # pos order signature
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/js/ControlButtons/AddSignatureButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/js/Popups/TemplateAddSignaturePopupWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/scss/sh_custom.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/xml/ControlButtons/AddSignatureButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/xml/Popups/TemplateAddSignaturePopupWidget.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_signature/static/src/xml/receipt.xml',

            # pos own customer
            'sh_pos_all_in_one_retail/static/sh_pos_own_customers/static/src/js/Screens/partner_list_screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_own_customers/static/src/js/db.js',

            # pos own product
            'sh_pos_all_in_one_retail/static/sh_pos_own_products/static/src/js/products_widget.js',

            # pos order label
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/js/ControlButton/AddLabelBtn.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/js/Popup/LabelPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/js/posWiget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/xml/controlButton/AddlabelButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/xml/Popups/LabelPopup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/xml/OrderReceipt.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_order_label/static/src/xml/OrderWidget.xml',

            # pos weight
            'sh_pos_all_in_one_retail/static/sh_pos_weight/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_weight/static/src/js/order_summary.js',
            'sh_pos_all_in_one_retail/static/sh_pos_weight/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_weight/static/src/xml/order_receipt.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_weight/static/src/xml/order_summary.xml',

            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/js/popups/ProductQtybagPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/js/Screens/product.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/js/Models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/xml/popups/ProductQtybagPopup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/xml/OrderLinesReceipt.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_product_qty_pack/static/src/xml/ProductItem/ProductItem.xml',

            # fronted cancel
            'sh_pos_all_in_one_retail/static/sh_pos_fronted_cancel/static/src/js/Screens/OrderListScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_fronted_cancel/static/src/scss/pos.scss',
            
            # customer order hystory
            'sh_pos_all_in_one_retail/static/sh_pos_customer_order_history/static/src/scss/pos.scss',
            
            'sh_pos_all_in_one_retail/static/sh_pos_customer_order_history/static/src/js/partner_list_screen.js',
          
            'sh_pos_all_in_one_retail/static/sh_pos_customer_order_history/static/src/xml/partner_list_screen.xml',

            # product template
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/js/Screens/templateLine.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/js/Screens/templateScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/js/action_buttons.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/scss/pos_custom.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/xml/Screens/template_product_screen.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_product_template/static/src/xml/action_buttons.xml',

            # pos secondary UOM
            'sh_pos_all_in_one_retail/static/sh_pos_secondary/static/src/js/ControlButton/ChangeUOMButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_secondary/static/src/js/Screens/ProductItem.js',
            'sh_pos_all_in_one_retail/static/sh_pos_secondary/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_secondary/static/src/xml/ControlButton/ChangeUOMButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_secondary/static/src/xml/OrderLinesReceipt.xml',

            # cash in out 
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/ControlButttons/CashInOutStatementButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/ControlButttons/PaymentsButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/Popups/CashInOutOptionStatementPopupWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/Popups/CashOpeningPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/Popups/TransactionPopupWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/Screens/CashInOutStatementReceipt.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/js/Screens/screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/ControlButtons/CashInOutStatementButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/ControlButtons/PaymentsButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/popups/CashInOutOptionStatementPopupWidget.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/popups/TransactionPopupWidget.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/Screens/CashInOutStatementReceipt.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_cash_in_out/static/src/xml/Screens/ReceiptScreen.xml',
            
            'sh_pos_all_in_one_retail/static/sh_pos_tags/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_tags/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_tags/static/src/js/products_widget.js',

            # Whatsapp integration
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/js/Popup/wapp_message_popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/js/Screens/partner_list_screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/js/Screens/receipt_screen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/xml/Popup/wapp_message_popup.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/xml/Screens/partner_list_screen.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_whatsapp_integration/static/src/xml/Screens/receipt_screen.xml',

            # rounding
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/js/OrderDetails.js',
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/js/PaymentScreenStatus.js',
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/js/Screeens/PaymentScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_rounding/static/src/xml/pos.xml',

            # line price list
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/js/Screens/productScreen/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/js/DB.js',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/js/popup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/xml/orderline.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_line_pricelist/static/src/xml/popup.xml',

            'sh_pos_all_in_one_retail/static/sh_pos_direct_login/static/src/js/Popups/close_popup.js',

            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/js/ControlButtons/CreateSoButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/js/popups/sh_pos_confirmPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/xml/ControlButtons/CreatePoButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_create_so/static/src/xml/Popups/sh_po_confirm_popup.xml',

            # display product code 
            'sh_pos_all_in_one_retail/static/sh_pos_product_code/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_code/static/src/xml/Screens/ProductItem.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_product_code/static/src/xml/Orderline.xml',

            # variants
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/Popups/variant_list.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/Popups/variant_pos.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/screens/ProductItem.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/screens/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/js/screens/ProductsWidget.js',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_product_variant/static/src/xml/variant_popup.xml',

            # Create Purchase Order
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/js/db.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/js/models.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/js/ControlButtons/CreatePoButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/js/popups/sh_pos_confirmPopup.js',
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/xml/ControlButtons/CreatePoButton.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_create_po/static/src/xml/Popups/sh_po_confirm_popup.xml',

            # creategory slider
            'sh_pos_all_in_one_retail/static/sh_pos_category_slider/static/src/js/CategoryButton.js',
            'sh_pos_all_in_one_retail/static/sh_pos_category_slider/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_category_slider/static/src/xml/CategoryButton.xml',

            # Maximum Discount
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/js/Screens/PartnerListScreen/PartnerDetailsEdit.js',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/js/Screens/PartnerListScreen/PartnerListScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/js/Screens/ProductScreen/ProductScreen.js',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/scss/pos.scss',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/xml/Screens/PartnerListScreen/PartnerDetailsEdit.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/xml/Screens/PartnerListScreen/PartnerLine.xml',
            'sh_pos_all_in_one_retail/static/sh_pos_customer_maximum_discount/static/src/xml/Screens/PartnerListScreen/PartnerListScreen.xml',

        ],

    },

    "images": [
        'static/description/splash-screen.gif',
        'static/description/splash-screen_screenshot.gif'

    ],
    "auto_install": False,
    "installable": True,
    "price": 214,
    "currency": "EUR",
}
