/*
     Desarrollado por Ing. Henerson Zambrano <zambranohender@gmail.com>

    The licence is in the file __manifest__.py
*/

odoo.define("pos_customer_required.PaymentScreen", function(require) {
    "use strict";

    const screens = require("point_of_sale.PaymentScreen");
  

    screens.prototype._isOrderValid = async function(isForceValidate){
        if (this.currentOrder.get_orderlines().length === 0 && this.currentOrder.is_to_invoice()) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Empty Order'),
                body: this.env._t(
                    'There must be at least one product in your order before it can be validated and invoiced.'
                ),
            });
            return false;
        }
        if (this.env.pos.config.require_customer != "no" && !this.currentOrder.get_partner()) {
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: this.env._t('Please select the Customer'),
                body: this.env._t(
                    'You need to select the customer before you can invoice or ship an order.'
                ),
            });
            if (confirmed) {
                this.selectPartner();
            }
        
            return false;
        }
        const splitPayments = this.paymentLines.filter(payment => payment.payment_method.split_transactions)
        if (splitPayments.length && !this.currentOrder.get_partner()) {
            const paymentMethod = splitPayments[0].payment_method
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: this.env._t('Customer Required'),
                body: _.str.sprintf(this.env._t('Customer is required for %s payment method.'), paymentMethod.name),
            });
            if (confirmed) {
                this.selectPartner();
            }
            return false;
        }

        if ((this.currentOrder.is_to_invoice() || this.currentOrder.is_to_ship()) && !this.currentOrder.get_partner()) {
            const { confirmed } = await this.showPopup('ConfirmPopup', {
                title: this.env._t('Please select the Customer'),
                body: this.env._t(
                    'You need to select the customer before you can invoice or ship an order.'
                ),
            });
            if (confirmed) {
                this.selectPartner();
            }
            return false;
        }

        var customer = this.currentOrder.get_partner()
       /* if (this.currentOrder.is_to_ship() && !(customer.name && customer.street && customer.city && customer.country_id)) {
            this.showPopup('ErrorPopup', {
                title: this.env._t('Incorrect address for shipping'),
                body: this.env._t('The selected customer needs an address.'),
            });
            return false;
        }*/

        if (!this.currentOrder.is_paid() || this.invoicing) {
            return false;
        }

        if (this.currentOrder.has_not_valid_rounding()) {
            var line = this.currentOrder.has_not_valid_rounding();
            this.showPopup('ErrorPopup', {
                title: this.env._t('Incorrect rounding'),
                body: this.env._t(
                    'You have to round your payments lines.' + line.amount + ' is not rounded.'
                ),
            });
            return false;
        }

        // The exact amount must be paid if there is no cash payment method defined.
        if (
            Math.abs(
                this.currentOrder.get_total_with_tax() - this.currentOrder.get_total_paid()  + this.currentOrder.get_rounding_applied()
            ) > 0.00001
        ) {
            var cash = false;
            for (var i = 0; i < this.env.pos.payment_methods.length; i++) {
                cash = cash || this.env.pos.payment_methods[i].is_cash_count;
            }
            if (!cash) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t('Cannot return change without a cash payment method'),
                    body: this.env._t(
                        'There is no cash payment method available in this point of sale to handle the change.\n\n Please pay the exact amount or add a cash payment method in the point of sale configuration'
                    ),
                });
                return false;
            }
        }

        // if the change is too large, it's probably an input error, make the user confirm.
        if (
            !isForceValidate &&
            this.currentOrder.get_total_with_tax() > 0 &&
            this.currentOrder.get_total_with_tax() * 1000 < this.currentOrder.get_total_paid()
        ) {
            this.showPopup('ConfirmPopup', {
                title: this.env._t('Please Confirm Large Amount'),
                body:
                    this.env._t('Are you sure that the customer wants to  pay') +
                    ' ' +
                    this.env.pos.format_currency(this.currentOrder.get_total_paid()) +
                    ' ' +
                    this.env._t('for an order of') +
                    ' ' +
                    this.env.pos.format_currency(this.currentOrder.get_total_with_tax()) +
                    ' ' +
                    this.env._t('? Clicking "Confirm" will validate the payment.'),
            }).then(({ confirmed }) => {
                if (confirmed) this.lockedValidateOrder(true);
            });
            return false;
        }

        if (!this.currentOrder._isValidEmptyOrder()) return false;

        return true;
                }
          
                return screens;
        });

    