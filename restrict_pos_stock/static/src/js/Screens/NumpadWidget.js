odoo.define("restrict_pos_stock.NumpadWidget", function (require) {
    "use strict";

    const NumpadWidget = require("point_of_sale.NumpadWidget");
    const Registries = require("point_of_sale.Registries");
    const { onMounted } = owl;

    const SHNumpadWidget = (NumpadWidget) =>
        class extends NumpadWidget {
            setup() {
                super.setup();
            }
            
            get hasPriceControlRights() {
                return false;
            }
        };

    Registries.Component.extend(NumpadWidget, SHNumpadWidget);
    
    return SHNumpadWidget

});