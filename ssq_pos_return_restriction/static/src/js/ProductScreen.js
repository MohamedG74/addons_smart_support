odoo.define('ssq_pos_return_restriction.ProductScreen', function(require) {
    'use strict';

    const ProductScreen = require('point_of_sale.ProductScreen');
    const RefundButton = require('point_of_sale.RefundButton');
    const ProductInfoButton = require('point_of_sale.ProductInfoButton');
    //const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');

    ProductScreen.addControlButton({
        component: RefundButton,
        condition: function () {
            var cashier = this.env.pos.get_cashier();
            var has_refund_control_rights = true;
            if (this.env.pos.config.is_return_allowed_control) {
                has_refund_control_rights = false;
                if (this.env.pos.config.return_allowed_employee_ids.includes(cashier.id)) {
                    has_refund_control_rights = true;
                }
            }
            return has_refund_control_rights;
        },
        position: ['replace', 'RefundButton'],
    });
    ProductScreen.addControlButton({
        component: ProductInfoButton,
        condition: function () {
            if (this.env.pos.get_cashier().role == 'manager') {
               return true;  
            }
            return false;
        },
        position: ['replace', 'ProductInfoButton'],
    });    


});
