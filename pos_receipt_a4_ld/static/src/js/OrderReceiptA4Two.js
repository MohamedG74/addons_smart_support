odoo.define('point_of_sale.OrderReceiptA4Two', function (require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt');
    const Registries = require('point_of_sale.Registries');

    class OrderReceiptA4Two extends OrderReceipt {
        constructor() {
            super(...arguments);
        }
    }

    OrderReceiptA4Two.template = 'OrderReceiptA4Two';

    Registries.Component.add(OrderReceiptA4Two);

    return OrderReceiptA4Two;
});
