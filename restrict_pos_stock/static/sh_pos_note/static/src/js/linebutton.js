odoo.define("sh_pos_note.LineButton", function (require) {
    "use strict";

    const PosComponent = require("point_of_sale.PosComponent");
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require("point_of_sale.Registries");
    const RefundButton = require("point_of_sale.RefundButton");
    const OrderlineCustomerNoteButton = require("point_of_sale.OrderlineCustomerNoteButton");
    const ProductScreen = require('point_of_sale.ProductScreen');

    ProductScreen.addControlButton({
        component: OrderlineCustomerNoteButton,
        condition: function () {
            var has_refund = false;
            return has_refund;
        },
        position: ['replace', 'OrderlineCustomerNoteButton'],
    });
    
    ProductScreen.addControlButton({
        component: RefundButton,
        condition: function () {
            var has_refund = false;
            return has_refund;
        },
        position: ['replace', 'RefundButton'],
    });

});
