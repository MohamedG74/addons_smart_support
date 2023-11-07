odoo.define("sh_pos_wh_stock.models", function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");
    var utils = require("web.utils");
    var round_pr = utils.round_precision;
    var field_utils = require("web.field_utils");
    var { Gui } = require('point_of_sale.Gui');


    const shPosOrderlinewhstock = (Orderline) => class shPosOrderlinewhstock extends Orderline {
        constructor(attr, options) {
            super(...arguments);
            this.enbale_nagative_saling = false
            this.mounted()
        }
        mounted(){
            setTimeout(() => {
                $('li.orderline.selected').find('.sh_orderline_icons').slideUp()
                
                $("li.orderline").mouseover(function () {
                    $(this).find('.sh_orderline_icons').slideDown("slow", function () {
                        $(this).find('.sh_orderline_icons').addClass('selected')
                    });
    
                });
                $("li.orderline").mouseleave(function () {
                    if (!$(this).hasClass('selected')) {
                        $(this).find('.sh_orderline_icons').slideUp("slow", function () {
                            $(this).find('.sh_orderline_icons').removeClass('selected')
                        });
                    }
    
                });
            }, 100);
        }
        get_image_url(product_id) {
            return window.location.origin + "/web/image?model=product.product&field=image_128&id=" + product_id;
        }
        set_quantity(quantity, keep_price) {
            var self = this;
            var unit = this.get_unit();
            if (quantity !== 'remove' && this.pos.config.sh_display_stock) {
                var quant = typeof (quantity) === 'number' ? quantity : (field_utils.parse.float('' + (quantity ? quantity : 0)));

                var quant_by_product_id = this.pos.db.quant_by_product_id[this.product.id];
                var qty_available = quant_by_product_id ? quant_by_product_id[this.pos.config.sh_pos_location[0]] : 0;

                var decimals = this.pos.dp["Product Unit of Measure"];
                var rounding = Math.max(unit.rounding, Math.pow(10, -decimals));


                if (this.pos.config.sh_multi_qty_enable) {
                    if (self.product.sh_minimum_qty_pos && this.pos.config.sh_pos_enable_min_qty) {
                        if (quant == 1) {
                            if (self.order && !self.order.get_selected_orderline()) {
                                quantity = self.product.sh_minimum_qty_pos
                            }else{
                                if (quantity < self.product.sh_minimum_qty_pos){
                                    quantity = self.product.sh_minimum_qty_pos
                                }
                            }
                        }
                    }
                    
                    var qty = parseInt(this.product.sh_multiples_of_qty) || quantity
                    
                    if (qty) {
                        if (qty <= quant) {
                            if (quant / qty == parseInt(quant / qty)) {
                                var loop = quant / qty
                            } else {
                                var loop = quant / qty + 1
                            }
                            for (var i = 2; i <= loop; i++) {
                                var val = qty * i
                                quantity = val
                                quant = val
                            }
                        }
                        else {
                            if (quantity !== 'remove'){
                                quantity = qty
                                quant = qty
                            }else{
                                quant = typeof (quantity) === 'number' ? quantity : (field_utils.parse.float('' + (quantity ? quantity : 0)));
                            }
                        }
                    }
                    
                }

                if (round_pr(quant, rounding) && this.pos.config.sh_show_qty_location && this.product.type == "product" && !self.product.is_added) {
                    if (qty_available - round_pr(quant, rounding) >= this.pos.config.sh_min_qty) {
                        super.set_quantity(quantity, keep_price)
                    }else{ 
                        if (self.quantity && self.quantity > 0){
                            console.log(' set quantity ')
                        }
                        if(!self.enbale_nagative_saling){
                            this.order.low_qty_shown = true
                            if (this.order.low_qty_shown){
                                Gui.showPopup("QuantityWarningPopup", {
                                    line: self,
                                    product: this.product,
                                    quantity: round_pr(quant, rounding),
                                    product_image: this.get_image_url(this.product.id),
                                }).then(function (solverd) {
                                    self.order.low_qty_shown = false
                                })
                            }
                        }
                    }
                    this.product["is_added"] = false;
                }else{
                    super.set_quantity(quantity, keep_price)
                }
                self.product["is_added"] = false;
            }else{
                this.product["is_added"] = false;
                if (this.pos.config.sh_multi_qty_enable && quantity !== 'remove') {
                    if (self.product.sh_minimum_qty_pos && this.pos.config.sh_pos_enable_min_qty) {
                        if (quant == 1) {
                            if (self.order && !self.order.get_selected_orderline()) {
                                quantity = self.product.sh_minimum_qty_pos
                            }else{
                                if (quantity < self.product.sh_minimum_qty_pos){
                                    quantity = self.product.sh_minimum_qty_pos
                                }
                            }
                        }
                    }
                    
                    var qty = parseInt(this.product.sh_multiples_of_qty) || quantity
                    
                    if (qty) {
                        if (qty <= quant) {
                            if (quant / qty == parseInt(quant / qty)) {
                                var loop = quant / qty
                            } else {
                                var loop = quant / qty + 1
                            }
                            for (var i = 2; i <= loop; i++) {
                                var val = qty * i
                                quantity = val
                                quant = val
                            }
                        }
                        else {
                            if (quantity !== 'remove'){
                                quantity = qty
                                quant = qty
                            }else{
                                quant = typeof (quantity) === 'number' ? quantity : (field_utils.parse.float('' + (quantity ? quantity : 0)));
                            }
                        }
                    }
                    
                }
                super.set_quantity(quantity, keep_price)
            }
            return true
        }
    }
    Registries.Model.extend(Orderline, shPosOrderlinewhstock);

    const shPosGlovalStateWhStock = (PosGlobalState) => class shPosGlovalStateWhStock extends PosGlobalState {
        async _processData(loadedData) {
            super._processData(...arguments)
            var self = this;
            self.db.add_qunats(loadedData['stock.quant']);
            self.db.add_warehouse(loadedData['stock.warehouse']);
            self.db.add_location(loadedData['stock.location']);
            self.db.add_picking_types(loadedData['stock.picking.type']);
        }
        get_cashier_user_id() {
            return this.user.id || false;
        }
    }
    Registries.Model.extend(PosGlobalState, shPosGlovalStateWhStock);

});
