odoo.define("wb_portal.WBSampleButton",function(require){
"use strict";


        const PosComponent= require("point_of_sale.PosComponent");
        const ProductScreen=require("point_of_sale.ProductScreen");
        const Registries=require("point_of_sale.Registries");
        const { useListener }=require("@web/core/utils/hooks");

        class WBSampleButton extends PosComponent{
                setup(){
                        super.setup();
                        useListener("click",this.wb_sample_button_click);    
                }
                async  wb_sample_button_click(){
                        this.showPopup("ErrorPopup",{
                                title:"Error message",
                                body:"The simple Error message screen",
                        });
                }
       

       
        }

        WBSampleButton.template="WBSampleButton";
        ProductScreen.addControlButton({
            component:WBSampleButton,
            position:["after","OrderlineCustomerNoteButton"],

        });
        Registries.Component.add(WBSampleButton);
        return WBSampleButton;
});