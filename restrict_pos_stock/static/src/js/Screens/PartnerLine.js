

odoo.define("restrict_pos_stock.partner_line_screen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const PartnerLine = require("point_of_sale.PartnerLine");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PosPartnerLine = (PartnerLine) =>
        class extends PartnerLine {
            constructor() {
                super(...arguments);
                var self = this;

            }

            getRole(){
                var cashier = this.env.pos.get_cashier();
                return cashier.role == "manager";
            }

        };

    Registries.Component.extend(PartnerLine, PosPartnerLine);

});
