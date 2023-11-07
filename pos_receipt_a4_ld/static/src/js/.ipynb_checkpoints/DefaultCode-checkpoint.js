odoo.define('pos_receipt_a4_ld.default_code', function (require) {
"use strict";

var models = require('point_of_sale.models');

models.load_fields('product.product', 'default_code');

var _super_orderline = models.Orderline.prototype;
models.Orderline = models.Orderline.extend({
    export_for_printing: function() {
        var line = _super_orderline.export_for_printing.apply(this,arguments);
        line.product_default_code = this.get_product().default_code;
        return line;
    },
});

});
