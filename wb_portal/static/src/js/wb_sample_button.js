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
               var res = await this.rpc({
                        route:"/pos/rpc/example",
                        params:{},
                        });
                        // res.forEach(function(value) {
                        //         console.log("Record ----->",value)
                                
                        // });
                        var multi_lang_list=[];

                        res.forEach(function(value){
                                multi_lang_list.push({"id":value.id,
                        "label":value.name,"item":value});
                        });
                        console.log("--------------------")
                        console.log(multi_lang_list);
                       var {confirmed,payload:SelectedOption}= await this.showPopup("SelectionPopup",{
                                title:"Choose language",
                                list:multi_lang_list
                       })
                       console.log(confirmed,SelectedOption);
                       this.showPopup("ErrorPopup",{
                        title:"You should enter product",
                        body:"This is an maessage "

                       })

        }// end of event
}//end of button class
        WBSampleButton.template="WBSampleButton";
        ProductScreen.addControlButton({
            component:WBSampleButton,
            position:["after","OrderlineCustomerNoteButton"],
        });
        Registries.Component.add(WBSampleButton);
        return WBSampleButton;
});

