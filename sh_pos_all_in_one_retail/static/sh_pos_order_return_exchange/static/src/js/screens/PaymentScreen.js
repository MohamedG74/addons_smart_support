odoo.define('sh_pos_order_return_exchange.paymentScreen', function(require, factory) {
    'use strict';
    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    const PosReturnPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor() {
                super(...arguments);
            }
            cancel_return_order() {
                var self = this;

                if (this.env.pos.get_order() && this.env.pos.get_order().get_orderlines() && this.env.pos.get_order().get_orderlines().length > 0) {
                    var orderlines = this.env.pos.get_order().get_orderlines();
                    _.each(orderlines, function (each_orderline) {
                        if (self.env.pos.get_order().get_orderlines()[0]) {
                            self.env.pos.get_order().remove_orderline(self.env.pos.get_order().get_orderlines()[0]);
                        }
                    });
                }
                self.env.pos.get_order().is_return_order(false);
                self.env.pos.get_order().return_order = false;
                self.env.pos.get_order().is_exchange_order(false);
                self.env.pos.get_order().exchange_order = false;
                self.env.pos.get_order().set_old_pos_reference(false);
                self.showScreen("ProductScreen");
            }
            async _finalizeValidation() {
                await super._finalizeValidation();
                var self = this;

                if (this.currentOrder.return_order) {
                    this.currentOrder.is_return_order(true);
                    if (this.currentOrder.old_pos_reference) {
                        this.currentOrder.set_old_pos_reference(this.currentOrder.old_pos_reference);
                        this.currentOrder.set_old_sh_uid(this.currentOrder.old_sh_uid);
                    }
                }
                if (this.currentOrder.exchange_order) {
                    this.currentOrder.is_exchange_order(true);
                    if (this.currentOrder.old_pos_reference) {
                        this.currentOrder.set_old_pos_reference(this.currentOrder.old_pos_reference);
                        this.currentOrder.set_old_sh_uid(this.currentOrder.old_sh_uid);
                    }
                }
            }
        };

    Registries.Component.extend(PaymentScreen, PosReturnPaymentScreen);
    
});