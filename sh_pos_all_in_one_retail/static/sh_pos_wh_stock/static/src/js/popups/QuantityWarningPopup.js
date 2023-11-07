odoo.define("sh_pos_wh_stock.QuantityWarningPopup", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");

    // const { useSubEnv, } = owl;


    class QuantityWarningPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup(...arguments)
            this.product_quantity = this.props.quantity;
            this.product = this.props.product;
            this.line = this.props.line;
            // useSubEnv({ attribute_components: [] });
        }
        put_order() {
            var self = this;
            var selectedOrder = self.env.pos.get_order();
            self.product["is_added"] = true;
            var newlocationDIC = {}
            if (this.line && this.line.product.id == this.product.id) {
                newlocationDIC[this.env.pos.config.sh_pos_location[0]] = 0 - this.product_quantity

                this.line.set_quantity(this.product_quantity);
            } else {
                if (this.line && this.line.price > 0) {
                    this.product.pos.get_order().add_product(this.product)
                    newlocationDIC[this.env.pos.config.sh_pos_location[0]] = 0 - 1
                }
            }
            this.env.pos.db.quant_by_product_id[this.product.id] = newlocationDIC
            this.confirm()
        }
        cancel() {
            super.cancel()
            this.env.pos.get_order().remove_orderline(this.line);
        }
    }
    QuantityWarningPopup.template = "QuantityWarningPopup";

    Registries.Component.add(QuantityWarningPopup);

    return QuantityWarningPopup
})