odoo.define("sh_pos_order_return_exchange.popup", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const AbstractAwaitablePopup = require("point_of_sale.AbstractAwaitablePopup");

    class ReturnOrderPopup extends AbstractAwaitablePopup {
        setup() {
            super.setup(arguments);
            this.lines = this.props.lines;
            this.order = this.props.order;
            this.no_return_line_id = [];
            this.return_line = [];
        }
        async confirm() {
            var self = this;
            
            _.each($(".return_data_line"), function (each_data_line) {
                if (each_data_line.children[4].children[0].value != "0" && each_data_line.children[4].children[0].value != "") {
                    var order_line = self.env.pos.db.order_line_by_id[each_data_line.dataset.line_id];
                    if (!order_line) {
                        order_line = self.env.pos.db.order_line_by_uid[each_data_line.dataset.line_id];
                    }
                    
                    order_line["old_qty"] = order_line["qty"];
                    order_line["qty"] = each_data_line.children[4].children[0].value;
                    self.return_line.push(order_line);
                } else {
                    self.no_return_line_id.push(parseInt(each_data_line.dataset.line_id));
                }
            });
            
            self.return_exchange_product();
             
            super.confirm()
        }
        async click_complete_return() {
            var self = this;
            var current_order = self.env.pos.get_order();
            if (document.getElementById("return_radio") && document.getElementById("return_radio").checked) {
                current_order.is_return = true;
                current_order.is_exchange = false;
            }else{
                current_order.is_return = false;
                current_order.is_exchange = true;
            }
            await _.each($(".return_data_line"), function (each_data_line) {
                if (each_data_line.children[2].children[0].value != "0") {
                    var order_line = self.env.pos.db.order_line_by_id[each_data_line.dataset.line_id];
                    if (!order_line) {
                        order_line = self.env.pos.db.order_line_by_uid[each_data_line.dataset.line_id];
                    }
                    order_line["qty"] = each_data_line.children[1].innerText;
                    self.return_line.push(order_line);
                } else {
                    self.no_return_line_id.push(parseInt(each_data_line.dataset.line_id));
                }
            });
            self.return_exchange_product();
            this.cancel()
        }
        async return_exchange_product() {
            var self = this;
            var order_id;
            await _.each($(".return_data_line"), function (each_data_line) {
                order_id = each_data_line.dataset.order_id;
            });
            
            var order_data = self.env.pos.db.order_by_uid[order_id];
            if (!order_data) {
                order_data = self.env.pos.db.order_by_id[order_id];
            }
            var current_order = self.env.pos.get_order();

            if (self.env.pos.get_order() && self.env.pos.get_order().get_orderlines() && self.env.pos.get_order().get_orderlines().length > 0) {
                var orderlines = self.env.pos.get_order().get_orderlines();
                await _.each(orderlines, function (each_orderline) {
                    if (self.env.pos.get_order().get_orderlines()[0]) {
                        self.env.pos.get_order().remove_orderline(self.env.pos.get_order().get_orderlines()[0]);
                    }
                });
            }
            
            _.each(self.return_line, function (each_line) {
                if (current_order.is_return) {
                    current_order["return_order"] = true;
                }
                if (current_order.is_exchange) {
                    current_order["exchange_order"] = true;
                }
                var product = self.env.pos.db.get_product_by_id(each_line.product_id[0]);
                if (!product) {
                    product = self.env.pos.db.get_product_by_id(each_line.product_id);
                }
                current_order.add_product(product, {
                    quantity: -each_line.qty,
                    price: each_line.price_unit,
                    line_id: each_line.id,
                    old_line_id: each_line.sh_line_id,
                    discount: each_line.discount,
                });
                
                if (order_data && order_data.partner_id && order_data.partner_id[0]) {
                    self.env.pos.get_order().set_partner(self.env.pos.db.get_partner_by_id(order_data.partner_id[0]));
                }

                if (order_data && order_data.user_id_custom && order_data.user_id_custom[0]) {
                    var orderlins = self.env.pos.get_order().get_orderlines();
                    for(var i = 0; i < orderlins.length; i++){
                        if(orderlins[i] != undefined){
                            orderlins[i].set_line_user(self.env.pos.employee_by_idn[order_data.user_id_custom[0]]);
                        }
                    }
                }
               
                if (current_order.is_exchange && $("#exchange_checkbox")[0].checked) {
                    current_order.add_product(product, {
                        quantity: each_line.qty,
                        price: each_line.price_unit,
                        merge: false,
                        discount: each_line.discount,
                    });
                }

                if (each_line.old_qty) {
                    each_line.qty = each_line.old_qty;
                }
            });
            if (order_data){
                current_order.old_sh_uid = order_data.sh_uid;
                current_order.old_pos_reference = order_data.pos_reference;
            }
            self.trigger("close-temp-screen");
            if (current_order.return_order) {
                self.showScreen('PaymentScreen')
            }
        }
        updateReturnQty(event) {
            var self = this;
            if (self.env.pos.get_order().is_return && !self.env.pos.config.sh_return_more_qty) {
                if (event.currentTarget.value) {
                    if (parseInt(event.currentTarget.value) > parseInt(event.currentTarget.closest("tr").children[1].innerText)) {
                        event.currentTarget.classList.add("more_qty");
                        event.currentTarget.value = "";
                    } else {
                        event.currentTarget.classList.remove("more_qty");
                    }
                }
            }

            if (self.env.pos.get_order().is_exchange) {
                if (event.currentTarget.value) {
                    if (parseInt(event.currentTarget.value) > parseInt(event.currentTarget.closest("tr").children[1].innerText)) {
                        event.currentTarget.classList.add("more_qty");
                        event.currentTarget.value = "";
                    } else {
                        event.currentTarget.classList.remove("more_qty");
                    }
                }
            }
        }
    }

    ReturnOrderPopup.template = "ReturnOrderPopup";
    Registries.Component.add(ReturnOrderPopup);

    return ReturnOrderPopup

});
