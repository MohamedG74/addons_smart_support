odoo.define("sh_pos_wh_stock.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const { useListener } = require("@web/core/utils/hooks");
    const { onMounted } = owl;
    const { identifyError } = require('point_of_sale.utils');
    const { ConnectionLostError, ConnectionAbortedError } = require('@web/core/network/rpc_service')

    const WHStockProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            setup() {
                super.setup(...arguments)
                useListener('infoproduct', this._infoproduct);
            }
            async _infoproduct(event){
                const product = event.detail;
                try {
                    const info = await this.env.pos.getProductInfo(product, 1);             
                    this.showPopup('ProductInfoPopup', { info: info , product: product });
                } catch (e) {
                    if (identifyError(e) instanceof ConnectionLostError||ConnectionAbortedError) {
                        this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Network Error'),
                            body: this.env._t('Cannot access product information screen if offline.'),
                        });
                    } else {
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Unknown error'),
                            body: this.env._t('An unknown error prevents us from loading product information.'),
                        });
                    }
                }
            }
            async _updateSelectedOrderline(event) {                
                setTimeout(function() {
                    $(".orderlines table tr td.product-code").each(function(index, element) {
                        if ($.trim($(element).text()) == "Discount") {
                            $(element).closest(".orderline").hide();
                        };
                    });
                    
                }, 500); // delay the execution by 1 second (1000 milliseconds)
                super._updateSelectedOrderline(event);                               
            }
            async _clickProduct(event) 
            {
                $(".orderlines table tr td.product-code").each(function(index,element){if($.trim($(element).text()) == "Discount"){
                    //$(element).closest(".orderline").appendTo('ul.orderlines');
                    $(element).closest(".orderline").hide();
                };});

                var orderlines = this.env.pos.get_order().get_orderlines();
                
                for(var i = 0; i < orderlines.length; i++){
                    if((event.detail.id == orderlines[i].get_product().id) && !orderlines[i].is_secondary){
                        return this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('تم اضافة المنتج من قبل'),
                        });
                    }
                }
                
                //const orderline = this.env.pos.get_order().get_selected_orderline();
                //if (orderline) {
                    const product = event.detail;
                    //const quantity = orderline.get_quantity();
                    const warehouse = this.env.pos.config.warehouse_id[1];
                    const allow_or_no = this.env.pos.config.smart_without_stock;                    
                    try {
                        const info = await this.env.pos.getProductInfo(product, 1);             
                        const qty = info.productInfo.warehouses.filter(function(x){ return x.name == warehouse})[0];
                        if(qty.available_quantity <= 0 && !allow_or_no){
                            return this.showPopup('ErrorPopup', {
                                title: this.env._t('Error'),
                                body: this.env._t('You are not allowed to sell product without stock.'),
                            });
                        }
                    } catch (e) {
                        if (identifyError(e) instanceof ConnectionLostError||ConnectionAbortedError) {
                            this.showPopup('OfflineErrorPopup', {
                                title: this.env._t('Network Error'),
                                body: this.env._t('Cannot access product information screen if offline.'),
                            });
                        } else {
                            this.showPopup('ErrorPopup', {
                                title: this.env._t('Unknown error'),
                                body: this.env._t('An unknown error prevents us from loading product information.'),
                            });
                        }
                    }
                //}     
                super._clickProduct(event);
            }
            _setValue(val) 
            {
                if (this.currentOrder.get_selected_orderline() && this.env.pos.numpadMode === 'discount' ) {
                    let product_discount = 100;
                    if(this.currentOrder.get_selected_orderline().get_product().sh_product_discount){
                        product_discount = this.currentOrder.get_selected_orderline().get_product().sh_product_discount;
                    }
                    let category_discount = 100;
                    if(this.currentOrder.get_selected_orderline().get_product().pos_categ_id){
                        category_discount = this.env.pos.db.get_category_by_id(this.currentOrder.get_selected_orderline().get_product().pos_categ_id[0]).sh_category_discount;
                    }
                    let allowed = "Product: "+(product_discount)+"% , Category: "+(category_discount)+"%";
                    if(val > product_discount || val > category_discount){
                        return this.showPopup('ErrorPopup', {
                            title : this.env._t("Discount Limit Reached"),
                            body  : this.env._t("The discount limit allowed ("+allowed+") is reached."),
                        });
                    }
                }
                if (this.currentOrder.get_selected_orderline() && (this.env.pos.numpadMode === 'quantity' || this.env.pos.numpadMode === 'discount' )) {
                    if((this.currentOrder.get_selected_orderline().get_product().default_code == "DISC" || this.currentOrder.get_selected_orderline().get_product().default_code == "Discount") && val != 0 && val != null && val != "remove"){
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('لا يمكنك التعديل على الخصم'),
                        });
                    }
                } 
                super._setValue(val);
                
            }
            
        };

    Registries.Component.extend(ProductScreen, WHStockProductScreen);
    return ProductScreen

})