odoo.define('pos_fixed_discount.FixedDiscountButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const DiscountButton = require('pos_discount.DiscountButton');

    const shInheritDiscountButton = (DiscountButton) => class InheritDiscountButton extends DiscountButton {
        async apply_discount(pc) {
            if(!this.env.pos.get_order().get_partner() || this.env.pos.get_order().get_partner() == null){
                return this.showPopup('ErrorPopup', {
                    title : this.env._t("Customer Not Selected"),
                    body  : this.env._t("Please select customer before making discount"),
                });
            }
            let allowed  = "Branch: " + (this.env.pos.config.sh_branch_discount) + "% , User: "+(this.env.pos.get_cashier().sh_employee_discount) + "% , Customer: "+(this.env.pos.get_order().get_partner().sh_partner_discount) + "%";
            let customer_discount = this.env.pos.get_order().get_partner().sh_partner_discount;
            let branch_discount = this.env.pos.config.sh_branch_discount;
            let cashier_discount = this.env.pos.get_cashier().sh_employee_discount;
            if(pc > cashier_discount || pc > customer_discount || pc > branch_discount){
                return this.showPopup('ErrorPopup', {
                    title : this.env._t("Discount Limit Reached"),
                    body  : this.env._t("The discount limit allowed ("+allowed+") is reached."),
                });
            }
            super.apply_discount(pc);
        }
    }
    class NewDiscountButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this;
            const { confirmed, payload } = await this.showPopup('NumberPopup',{
                title: this.env._t('Discount Amount'),
                startingValue: this.env.pos.config.discount_pc,
                isInputSelected: true
            });
            if (confirmed) {
                const val = payload
                await self.apply_discount(val);
            }
        }

        async apply_discount(pc) {
            let euqlpercent = (pc / this.env.pos.get_order().get_subtotal()) * 100;
            if(!this.env.pos.get_order().get_partner() || this.env.pos.get_order().get_partner() == null){
                return this.showPopup('ErrorPopup', {
                    title : this.env._t("Customer Not Selected"),
                    body  : this.env._t("Please select customer before making discount"),
                });
            }
            let allowed  = "Branch: " + (this.env.pos.config.sh_branch_discount) + "% , User: "+(this.env.pos.get_cashier().sh_employee_discount) + "% , Customer: "+(this.env.pos.get_order().get_partner().sh_partner_discount) + "%";
            let customer_discount = this.env.pos.get_order().get_partner().sh_partner_discount;
            let branch_discount = this.env.pos.config.sh_branch_discount;
            let cashier_discount = this.env.pos.get_cashier().sh_employee_discount;
            if(euqlpercent > cashier_discount || euqlpercent > customer_discount || euqlpercent > branch_discount){
                return this.showPopup('ErrorPopup', {
                    title : this.env._t("Discount Limit Reached"),
                    body  : this.env._t("The discount limit allowed ("+allowed+") is reached."),
                });
            }

            var order    = this.env.pos.get_order();
            var lines    = order.get_orderlines();
            var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
            if (product === undefined) {
                await this.showPopup('ErrorPopup', {
                    title : this.env._t("No discount product found"),
                    body  : this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                });
                return;
            }

            
            let discountValue = -pc;

            // Set the discount value in the order
            let x = this.env.pos.get_order();
            x.discount_value = discountValue;




            // Remove existing discounts
            lines.filter(line => line.get_product() === product)
                .forEach(line => order.remove_orderline(line));

            // Add one discount line per tax group
            var discount = -pc;          
            order.add_product(product, {
                price: discount,
                lst_price: 1,
                extras: {
                    price_manually_set: true,
                },
            });
            
            
            let linesByTax = order.get_orderlines_grouped_by_tax_ids();
            /*for (let [tax_ids, lines] of Object.entries(linesByTax)) {

                // Note that tax_ids_array is an Array of tax_ids that apply to these lines
                // That is, the use case of products with more than one tax is supported.
                let tax_ids_array = tax_ids.split(',').filter(id => id !== '').map(id => Number(id));

                //let baseToDiscount = order.calculate_base_amount(tax_ids_array, lines);

                // We add the price as manually set to avoid recomputation when changing customer.
                let discount = - pc;
                if (discount < 0) {
                    order.add_product(product, {
                        price: discount,
                        lst_price: discount,
                        tax_ids: tax_ids_array,
                        merge: false,
                        description:
                            `${pc}%, ` +
                            (tax_ids_array.length ?
                                _.str.sprintf(
                                    this.env._t('Tax: %s'),
                                    tax_ids_array.map(taxId => this.env.pos.taxes_by_id[taxId].amount + '%').join(', ')
                                ) :
                            this.env._t('No tax')),
                        extras: {
                            price_manually_set: true,
                        },
                    });
                }
            }*/
            if(pc == 0){
                var order    = this.env.pos.get_order();
                var lines    = order.get_orderlines();
                var product  = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
                lines.filter(line => line.get_product() === product)
                .forEach(line => order.remove_orderline(line));
            }
        }
    }
    NewDiscountButton.template = 'FixedDiscountButton';

    ProductScreen.addControlButton({
        component: NewDiscountButton,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(NewDiscountButton);
    
    Registries.Component.extend(DiscountButton, shInheritDiscountButton);

    return NewDiscountButton;
});
