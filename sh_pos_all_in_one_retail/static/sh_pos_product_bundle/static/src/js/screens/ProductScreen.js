
odoo.define("sh_pos_all_in_one_retail.sh_pos_product_bundle.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");

    const BundleStockProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            setup() {
                super.setup(...arguments);
                useListener("click-product-bundle-icon", this.on_click_show_bundle);
            }
            async on_click_show_bundle(event) {
                const product = event.detail;
                var self = this;
                let title = product.display_name;
                let product_id = product.id;
                let product_tmpl_id = product.product_tmpl_id;
                let bundle_by_product_id = this.env.pos.db.bundle_by_product_id[product_tmpl_id];

                let { confirmed, payload } = await this.showPopup("ProductBundlePopup", {
                    title: title,
                    'bundle_by_product_id': bundle_by_product_id,
                });

                if (confirmed) {
                } else {
                    return;
                }
            }
            async _clickProduct(event) {
                const product = event.detail;
                if (this.env.pos.config.enable_product_bundle && product && product.sh_is_bundle) {
                    var self = this;
                    let title = product.display_name;
                    var product_id = product.id;
                    var product_tmpl_id = product.product_tmpl_id;
                    let bundle_by_product_id = this.env.pos.db.bundle_by_product_id[product_tmpl_id];
                    let { confirmed, payload } = await this.showPopup("ProductQtyPopup", {
                        title: title,
                        price: product.lst_price.toFixed(2),
                        bundle_by_product_id: bundle_by_product_id
                    });

                    if (confirmed) {
                        var self = this;
                        // on confirm added all cart products in cart
                        var input_qty = $("#product_qty").val();
                        var lst_price = $("#product_price").val();

                        // get bundle products
                        await _.each($("#bundle_product_table").find("tr.data_tr"),async function (row) {
                            for (var i=0; i<$(row).find("input.qty_input").length;i++ ){
                                var $input = $(row).find("input.qty_input")[i]
                                var product_options = {};
                                product_options["price"] = 0.0;
                                product_options["quantity"] = $($input).val();
                                const product = self.env.pos.db.product_by_id[$(row).data("id")];
                                await self.env.pos.get_order().add_product(product, product_options);
                                var lines = self.env.pos.get_order().get_orderlines();
                                for (var i = 0; i < lines.length; i++) {
                                    if (lines[i].get_product().id === product.id) {
                                        lines[i].set_unit_price(0.0);
                                        lines[i].price_manually_set = true;
                                        return;
                                    }
                                }
                            }
                        });

                        // Add main product
                        const main_product = self.env.pos.db.product_by_id[product_id];
                        var product_options = {};
                        product_options["quantity"] = input_qty;
                        product_options["price"] = lst_price;

                        self.env.pos.get_order().add_product(main_product, product_options);
                        var lines = self.env.pos.get_order().get_orderlines();
                        for (var i = 0; i < lines.length; i++) {
                            if (lines[i].get_product() === product) {
                                lines[i].set_unit_price(lst_price);
                                lines[i].price_manually_set = true;
                                return;
                            }
                        }
                    } else {
                        return;
                    }
                } else {
                    super._clickProduct(event);
                }
            }
            async _setValue(val) {
                if (this.currentOrder.get_selected_orderline()) {
                    if (this.env.pos.numpadMode === "quantity") {
                        var self = this;
                        if (this.currentOrder.get_selected_orderline() && this.currentOrder.get_selected_orderline().get_product()) {
                            if (this.env.pos.get_order().get_selected_orderline() && this.env.pos.get_order().get_selected_orderline().product.sh_minimum_qty_pos && this.env.pos.config.sh_pos_enable_min_qty) {
                                var qty = parseInt(this.env.pos.get_order().get_selected_orderline().product.sh_minimum_qty_pos)
                                if (parseInt(val) < qty) {
                                    val = qty
                                }
                            }
                            var product = this.currentOrder.get_selected_orderline().get_product();
                            if (product.sh_is_bundle && this.env.pos.config.enable_product_bundle) {
                                var new_qty = val;
                                
                                var update_qty = new_qty ;
                                
                                var bundle_by_product_id = this.env.pos.db.bundle_by_product_id[product.product_tmpl_id];
                                await $.each(bundle_by_product_id, function (key, value) {
                                    var bundle_product = value[0];
                                    // Update Qty of other bundle product
                                    var lines = self.currentOrder.get_orderlines();
                                    for (var i = 0; i < lines.length; i++) {
                                        if (lines[i].get_product().id === bundle_product) {
                                            var new_qty = value[1] * update_qty;
                                            val = new_qty || val
                                        }
                                    }
                                });
                            } 
                        }
                    }
                }
                super._setValue(val)
            }
        };

    Registries.Component.extend(ProductScreen, BundleStockProductScreen);

})
