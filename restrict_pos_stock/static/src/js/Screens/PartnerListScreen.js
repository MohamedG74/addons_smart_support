

odoo.define("restrict_pos_stock.partner_list_screen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const PartnerListScreen = require("point_of_sale.PartnerListScreen");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PosPartnerListScreen = (PartnerListScreen) =>
        class extends PartnerListScreen {
            constructor() {
                super(...arguments);
                var self = this;

            }

            getRole(){
                var cashier = this.env.pos.get_cashier();
                return cashier.role == "manager";
            }

            editPartner(partner) {
                if(this.getRole()){
                    return super.editPartner(partner)
                }
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('Access Denied'),
                    body: this.env._t('You can\'t access customer details.'),
                });

            }


        };

    Registries.Component.extend(PartnerListScreen, PosPartnerListScreen);

});
