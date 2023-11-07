odoo.define('pos_receipt_a4_ld.client_data', function (require) {
"use strict";

var models = require('point_of_sale.models');

//

var _super_orderline = models.Order.prototype;
models.Order = models.Order.extend({
    export_for_printing: function() {
        var line = _super_orderline.export_for_printing.apply(this,arguments);
        //if(line.selectedClient != null){
            models.load_fields('res.partner', ['contact_address','phone','street']);
            line.client.street = this.get_client().street;
            line.client.phone = this.get_client().phone;            
        //}
        return line;
    },
});

});
