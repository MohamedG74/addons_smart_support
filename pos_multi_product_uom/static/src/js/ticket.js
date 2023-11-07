odoo.define('pos_multi_product_uom.ticket', function (require) {
	"use strict";
  var pos_model = require('point_of_sale.models');
  const { useState } = owl.hooks;
  var SuperOrderline = pos_model.Orderline.prototype;
  const models = require('point_of_sale.models');
  const Registries = require('point_of_sale.Registries');
  const Orderline = require('point_of_sale.Orderline');
  const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
  const ProductScreen = require('point_of_sale.ProductScreen');
  const NumberBuffer = require('point_of_sale.NumberBuffer');
  const TicketScreen = require('point_of_sale.TicketScreen');
  const { useListener, useAutofocus } = require('web.custom_hooks');
  const { posbus } = require('point_of_sale.utils');
  const { parse } = require('web.field_utils');
  var rpc = require('web.rpc');  
  const ticketScreeninhertie = (TicketScreen) =>
    
  class extends TicketScreen{
    constructor() {
        super(...arguments);
    }
    async _onClickOrder({ detail: clickedOrder }) {
        const orders = clickedOrder.get_orderlines();
           var self = this;
            
            var res = await rpc.query({
                model: 'pos.order.line',
                method: 'search_read',
                args: [[], []]
                
            }).then(function (products) {
                Object.keys(orders).forEach((item) => {
                    for (let i=0; i<products.length; i++){    
                        if (orders[item]['id'] === products[i]['id'] ){
                            orders[item].set_unit(products[i]['product_uom_id'][0]);    
                            // orders[item].uom_id = products[i]['product_uom_id'];
                            orders[item].product.uom_id = products[i]['product_uom_id']; 
                        }
                }
                   
                })

                
                if (!clickedOrder || clickedOrder.locked) {
                    if (self._state.ui.selectedSyncedOrderId == clickedOrder.backendId) {
                        self._state.ui.selectedSyncedOrderId = null;
                        
                    } else {
                        self._state.ui.selectedSyncedOrderId = clickedOrder.backendId;
                        }
                    if (!self.getSelectedOrderlineId()) {
                        // Automatically select the first orderline of the selected order.
                        const firstLine = clickedOrder.get_orderlines();
                        if (firstLine) {
                            self._state.ui.selectedOrderlineIds[clickedOrder.backendId] = firstLine.id;
                            
                        }
                    }
                    NumberBuffer.reset();
                } else {
                    self._setOrder(clickedOrder);
                }

            });
                
                                

             this.render();
            

            //  if (!clickedOrder || clickedOrder.locked) {
            //     if (this._state.ui.selectedSyncedOrderId == clickedOrder.backendId) {
            //         this._state.ui.selectedSyncedOrderId = null;
            //     } else {
            //         this._state.ui.selectedSyncedOrderId = clickedOrder.backendId;
            //     }
            //     if (!this.getSelectedOrderlineId()) {
            //         // Automatically select the first orderline of the selected order.
            //         const firstLine = clickedOrder.get_orderlines()[0];
            //         if (firstLine) {
            //             this._state.ui.selectedOrderlineIds[clickedOrder.backendId] = firstLine.id;
            //         }
            //     }
            //     NumberBuffer.reset();
            // } else {
            //     this._setOrder(clickedOrder);
            // }
         
            
        
        
       
        
    }
    async _onDoRefund() {
        const order = this.getSelectedSyncedOrder();
        for(let i=0; i<this.env.pos.units.length; i++){
            for(let j=0; j<order.orderlines.models.length; j++){
                var unit = this.env.pos.units[i];
                
                if(order.orderlines.models[j].uom_id == unit.id) {
                    var un_id = [unit.id,unit.name];
                    order.orderlines.models[j].product.uom_id = un_id;
                  
                if (!order) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    return this.render();
                }
                if (this._doesOrderHaveSoleItem(order)) {
                    this._prepareAutoRefundOnOrder(order);
                }
                const customer = order.get_client();
        
                const allToRefundDetails = this._getRefundableDetails(customer)
                
                
                if (allToRefundDetails.length == 0) {
                    this._state.ui.highlightHeaderNote = !this._state.ui.highlightHeaderNote;
                    return this.render();
                }
        
                // The order that will contain the refund orderlines.
                // Use the destinationOrder from props if the order to refund has the same
                // customer as the destinationOrder.
                const destinationOrder =
                    this.props.destinationOrder && customer === this.props.destinationOrder.get_client()
                        ? this.props.destinationOrder
                        : this.env.pos.add_new_order({ silent: true });
        
                // Add orderline for each toRefundDetail to the destinationOrder.
                for (const refundDetail of allToRefundDetails) {
                            
                var product = this.env.pos.db.get_product_by_id(refundDetail.orderline.productId);
                var options = this._prepareRefundOrderlineOptions(refundDetail);
                for(let i=0; i<order.orderlines.models.length; i++){
                    if (order.orderlines.models[i].id ===  refundDetail.orderline.id){
                        options["uom_id"] =    order.orderlines.models[i].uom_id;     
                        options["return"] = "yes";
                    }
                }
                
                destinationOrder.add_product(product, options);
                refundDetail.destinationOrderUid = destinationOrder.uid;
                           
                
                }    


                
        
                // Set the customer to the destinationOrder.
                if (customer && !destinationOrder.get_client()) {
                    destinationOrder.set_client(customer);
                    destinationOrder.updatePricelist(customer);
                }
        
                this._onCloseScreen(); 
            }
            }
            
        }
        
            
        
        
    }
    
  }
  Registries.Component.extend(TicketScreen, ticketScreeninhertie);
  
  return TicketScreen;

});