odoo.define("restrict_pos_stock.ticket_screen", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const TicketScreen = require("point_of_sale.TicketScreen");
    const InvoiceButton = require("point_of_sale.InvoiceButton");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PosTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            constructor() {
                super(...arguments);
                var self = this;

            }

            getDateDiff(order) {
                var a = moment();
                var b = moment(order.validation_date);
                return a.diff(b, 'days');
            }

            getRole(){
                var cashier = this.env.pos.get_cashier();
                return cashier.role == "manager";
            }

            getSalesPerson(order) {
                var self = this;
                if(order.user_id_custom){
                    if(this.env.pos.employee_by_idn[order.user_id_custom] != undefined){
                        return this.env.pos.employee_by_idn[order.user_id_custom].name;
                    }
                    /*for (var i = 0; i < this.env.pos.employee_by_id.length; i++) {
                        if (this.env.pos.employee_by_id[i].id == order.user_id_custom) {
                            return self.pos.employees[i].name;
                        }
                    }*/
                }
                return "-";
                
            }
            getTax(order){
                return this.env.pos.format_currency(order.amount_tax);
            }
            getBeforeTotal(order){
                return this.env.pos.format_currency(order.amount_total-order.amount_tax);
            }
            getMoveName(order) {
                return order.get_move_name();
                console.log(order);
                return order.account_movename ? order.account_movename : '-';
            }
            getMoveType(order) {
                return order.get_move_type();
            }
            getDeliveryStatus(order) {
                return order.get_move_delivery();
            }
            getNotes(order) {
                if(order.order_note != undefined){
                    if(order.order_note.toString()){
                        if(order.order_note.toString() != "false"){
                            return order.order_note;
                        }
                    }
                } 
                return "-";
            }
            _getSearchFields(){
                var fieldsnew = super._getSearchFields();
                fieldsnew.account_movename =  {
                    repr: (order) => order.account_movename,
                    displayName: this.env._t('Invoice Number'),
                    modelField: 'account_move.name'
                };
                fieldsnew.user_id_custom =  {
                    repr: (order) => getSalesPerson(order),
                    displayName: this.env._t('المندوب'),
                    modelField: 'user_id_custom.name'
                };

                return fieldsnew;
            }

        };

    Registries.Component.extend(TicketScreen, PosTicketScreen);
    
    const PosInvoiceButton = (InvoiceButton) =>
        class extends InvoiceButton {
            constructor() {
                super(...arguments);
                var self = this;

            }

            async _downloadInvoice(orderId) {
                console.log('nodl');
            }

        };

    Registries.Component.extend(InvoiceButton, PosInvoiceButton);

});
