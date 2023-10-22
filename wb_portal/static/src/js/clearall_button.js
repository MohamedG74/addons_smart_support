odoo.define("wb_portal.WBClearAllButton",function(require){
    "use strict";
    
    
            const PosComponent= require("point_of_sale.PosComponent");
            const ProductScreen=require("point_of_sale.ProductScreen");
            const Registries=require("point_of_sale.Registries");
            const { useListener }=require("@web/core/utils/hooks");
    
            class WBClearAllButton extends PosComponent{
                setup(){
                            super.setup();
                            useListener("click",this.wb_clear_button_click);    
                    }
                    async  wb_clear_button_click(){
                        console.log("Clearrrrrrrrrrrrrrrrr")
                        var current_order=this.env.pos.get_order();
                        current_order.orderlines.filter(line=>line.get_product()).forEach(single_line =>current_order.remove_orderline(single_line));     
                        
                }
    }
    
            WBClearAllButton.template="WBClearAllButton";
            ProductScreen.addControlButton({
                component:WBClearAllButton,
                position:["before","OrderlineCustomerNoteButton"],
    
            });
            Registries.Component.add(WBClearAllButton);
            return WBClearAllButton;
    });