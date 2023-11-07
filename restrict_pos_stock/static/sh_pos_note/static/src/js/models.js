odoo.define("sh_pos_note.Models", function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var PosDB = require('point_of_sale.DB');
    const PaymentScreen = require("point_of_sale.PaymentScreen");

    const shPosOrder = (Order) => class shPosOrder extends Order {
        to_invoice = true;
    
        init_from_JSON (json) {
           
            super.init_from_JSON(...arguments);
            if (json && json.order_note){
                this.order_note = json.order_note || ""
            }
            if (json && json.account_movename){
                this.account_movename = json.account_movename || ""
            }
            if (json && json.account_movetype){
                this.account_movetype = json.account_movetype || ""
            }
            if (json && json.account_movedelivery){
                this.account_movedelivery = json.account_movedelivery || ""
            }
            if (json && json.user_id_custom){
                this.user_id_custom = json.user_id_custom || ""
            }
            if (json && json.amount_tax){
                this.amount_tax = json.amount_tax || ""
            }
            if (json && json.amount_total){
                this.amount_total = json.amount_total || ""
            }
        }
        set_global_note (order_note) {
            this.order_note = order_note;
        }
        get_user_id_custom  () {
            var orderlines = this.get_orderlines();
            for(var i = 0; i < orderlines.length; i++){
                if(orderlines[i] != undefined){
                    if(orderlines[i].get_line_user()){
                        if(orderlines[i].get_line_user().id){
                            return orderlines[i].get_line_user().id;
                        }
                    }
                }
            }
            return null;
        }
        get_global_note  () {
            return this.order_note;
        }
        get_move_name  () {
            return this.account_movename;
        }
        get_move_type  () {
            return this.account_movetype == "out_refund" ? "مرتجع":"بيع";
        }
        get_move_delivery  () {
            if(this.account_movedelivery == "no"){
                return "لم يتم الاستلام";
            }
            if(this.account_movedelivery == "part"){
                return "تم الاستلام جزئياً";
            }
            if(this.account_movedelivery == "done"){
                return "تم الاستلام بالكامل";
            }
            return "-";
        }

        export_as_JSON () {
            const json = super.export_as_JSON(...arguments);
            json.order_note = this.get_global_note() || null;
            json.account_movename = this.get_move_name() || null;
            json.account_movetype = this.get_move_type() || null;
            json.account_movedelivery = this.get_move_delivery() || null;
            json.user_id_custom = this.get_user_id_custom() || null;
            return json;
        }

        export_for_printing() {
            var self = this;
            var orders = super.export_for_printing(...arguments);
        
            orders['order_global_note'] = self.get_global_note() || false
            
            return orders;
        }

        select_orderline(line){
            setTimeout(function() {
                $(".orderlines table tr td.product-code").each(function(index, element) {
                    if ($.trim($(element).text()) == "Discount") {
                        $(element).closest(".orderline").hide();
                    };
                });
            }, 500); // delay the execution by 1 second (1000 milliseconds)
            super.select_orderline(line);
        }

    }

    Registries.Model.extend(Order, shPosOrder);


    const shPosOrderLine = (Orderline) => class shPosOrderLine extends Orderline {
        
        init_from_JSON (json) {
            super.init_from_JSON(...arguments);
            if (json && json.line_note){
                this.line_note = json.line_note || ""
            }else{
                this.line_note = ""
            }
        }
        set_line_note (line_note) {
            this.line_note = line_note;
        }
        get_line_note  () {
            return this.line_note;
        }

        export_as_JSON () {
            const json = super.export_as_JSON(...arguments);
            json.line_note = this.get_line_note() || null;
            return json;
        }

        export_for_printing() {
        var self = this;
        var lines = super.export_for_printing(...arguments);
            
        lines['line_note'] = self.get_line_note() || false
        
        return lines
    }

    }

    Registries.Model.extend(Orderline, shPosOrderLine);

    const shNotePosGlobalState = (PosGlobalState) => class shNotePosGlobalState extends PosGlobalState {

        async _processData(loadedData) {
            await super._processData(...arguments);
            this.pre_defined_note_data_dict = loadedData['pre_defined_note_data_dict'] || [];
            this.db.all_note_names = loadedData['all_note_names'] || [];
        }
        
    }

    Registries.Model.extend(PosGlobalState, shNotePosGlobalState);

    
});
