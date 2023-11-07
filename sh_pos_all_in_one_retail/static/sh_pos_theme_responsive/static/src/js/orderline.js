odoo.define("sh_pos_theme_responsive.orderline", function (require) {
    "use strict";

    const Orderline = require("point_of_sale.Orderline");
    const Registries = require("point_of_sale.Registries");

    const PosOrderlineScreen = (Orderline) =>
        class extends Orderline {
            constructor() {
                super(...arguments);
            }
            imageUrl(product) {
                return `/web/image?model=product.product&field=image_128&id=${product.id}&write_date=${product.write_date}&unique=1`;
            }
            async removelineClick(event) {
                var self = this;
                event.stopPropagation();
                event.preventDefault();

                if($('.product[data-product-id="' + this.props.line.product.id + '"]').find(".sh_warehouse_display") && $('.product[data-product-id="' + this.props.line.product.id + '"]').find(".sh_warehouse_display")[0]){
                    $('.product[data-product-id="' + this.props.line.product.id + '"]').find(".sh_warehouse_display")[0].innerText = parseFloat($('.product[data-product-id="' + this.props.line.product.id + '"]').find(".sh_warehouse_display")[0].innerText) + this.props.line.quantity
                    if (this.env.pos.db.quant_by_product_id[this.props.line.product.id]){
                        var actual_quantity = this.env.pos.db.quant_by_product_id[this.props.line.product.id][this.env.pos.config.sh_pos_location[0]] = this.env.pos.db.quant_by_product_id[this.props.line.product.id][this.env.pos.config.sh_pos_location[0]]  + this.props.line.quantity
    
                        var dic = {
                            'product_id': this.props.line.product.id,
                            'location_id': this.env.pos.config.sh_pos_location[0],
                            'quantity': actual_quantity,
                            'other_session_qty':  this.props.line.quantity,
                            'manual_update': false
                        }
        
                        self.rpc({
                            model: 'sh.stock.update',
                            method: 'sh_update_manual_qty',
                            args: [self.env.pos.pos_session.id, dic]
                        })
                    }

                }

                this.trigger('select-line', { orderline: this.props.line });

                self.env.pos.get_order().remove_orderline(self.env.pos.get_order().get_selected_orderline())
            }
        };

    Registries.Component.extend(Orderline, PosOrderlineScreen);
});
