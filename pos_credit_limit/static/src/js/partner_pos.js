odoo.define('point_of_sale.PurchaseLimitPOS', function (require) {
    'use strict';

    const { parse } = require('web.field_utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const { useErrorHandlers } = require('point_of_sale.custom_hooks');
    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const utils = require('web.utils');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
//    var rpc = require('web.rpc')

    const PurchaseLimitPOS = (PaymentScreen) =>
    class extends PaymentScreen {

        async validateOrder() {
            await this.env.pos._loadPartners([this.currentOrder.get_partner().id]);
            const customer = this.currentOrder.get_partner();
            const amount = this.currentOrder.get_total_with_tax();
            const line = this.currentOrder.get_paymentlines();
            if(line.length == 0){
                return this.showPopup('ErrorPopup', {
                    title: this.env._t('لم يتم اختيار طريقة دفع'),
                    body: this.env._t("برجاء اختيار طريقة الدفع لاستكمال الطلب."),
                });
            }
            if(line[0].payment_method.id == 22){
                if(customer.credit_days >= customer.block_days){
                    return this.showPopup('ErrorPopup', {
                        title: this.env._t('Exceeding Credit Limit Days'),
                        body: this.env._t("Sorry the credit limit days allowed will cross the limit."),
                    });
                }
                if((customer.credit_amount + amount) > customer.credit_limit){
                    return this.showPopup('ErrorPopup', {
                        title: this.env._t('Exceeding Credit Limit Amount'),
                        body: this.env._t("Sorry the credit limit amount allowed will cross the limit."),
                    });    
                }
            }
            await super.validateOrder()
        }

    }
     Registries.Component.extend(PaymentScreen, PurchaseLimitPOS);
      return PaymentScreen;
});
