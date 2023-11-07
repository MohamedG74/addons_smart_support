odoo.define("restrict_pos_stock.summary_screen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const OrderSummary = require("point_of_sale.OrderSummary");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PosOrderSummary = (OrderSummary) =>
        class extends OrderSummary {
            constructor() {
                super(...arguments);
                var self = this;

            }
            getSalesPers() {
                if(this.props.order){
                    var orderlines = this.props.order.get_orderlines();
                    for(var i = 0; i < orderlines.length; i++){
                        if(orderlines[i] != undefined){
                            if(orderlines[i].get_line_user()){
                                if(orderlines[i].get_line_user().name){
                                    return orderlines[i].get_line_user().name;
                                }
                            }
                        }
                    }
                }else{
                    return "";
                }
                
            }
            getGlobalNote(){
                if(this.props.order){
                    return this.props.order.order_note;
                }
                return "-";
            }
            getWithout() {
                const totalWithoutTax = this.props.order.get_total_without_tax();
                return {
                    displayAmount: this.env.pos.format_currency(totalWithoutTax)
                };
            }
            getDiscNormal(){
                var total_disc = 0;
                if(this.props.order){
                    var orderlines = this.props.order.get_orderlines();
                    for(var i = 0; i < orderlines.length; i++){
                        if(orderlines[i] != undefined){
                            /*if(orderlines[i].get_discount_str() !== 0){
                                var before = orderlines[i].get_unit_display_price()*orderlines[i].get_quantity_str();
                                total_disc = total_disc + (orderlines[i].get_discount_str()/100*before);
                            }*/
                            if(orderlines[i].get_product().default_code == "Discount"){
                                total_disc = total_disc + Math.abs(orderlines[i].get_price_without_tax());
                            }
                        }
                    }
                }
                return total_disc;
            }
            check_discount(string){
                let discountRegex = /(\d+)%/i;
                let discountMatch = string.match(discountRegex);

                if (discountMatch) {
                // Discount percentage found
                let discountPercentage = discountMatch[1];
                    return discountPercentage;
                } else {
                // No discount percentage found
                 var disc = 0;
                 return disc;
                }
            }
            getDisc(){
                var discount_percent = 0;
                var orderlines = this.props.order.get_orderlines();
                var oline = -1;
                for(var i = 0; i < orderlines.length; i++){
                    if(orderlines[i] != undefined){
                        if(orderlines[i].get_product().default_code == "Discount"){
                            discount_percent = this.check_discount(orderlines[i].get_full_product_name());
                            oline = i;
                        }
                    }                    
                }
                
                if(discount_percent > 0 && oline != -1){
                    orderlines[oline].set_unit_price(0-(discount_percent * (this.props.order.get_total_without_tax()+this.getDiscNormal())) / 100);
                    return "("+discount_percent.toString()+"%) " + this.env.pos.format_currency((discount_percent * (this.props.order.get_total_without_tax()+this.getDiscNormal())) / 100);
                }

                
                return this.env.pos.format_currency(this.getDiscNormal());
            }
            getBefore(){
                var before = 0;
                if(this.props.order){
                    before = this.props.order.get_total_without_tax()+this.getDiscNormal();
                }                
                return this.env.pos.format_currency(before);
            }

        };

    Registries.Component.extend(OrderSummary, PosOrderSummary);

});
