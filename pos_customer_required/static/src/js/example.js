/*
    ejemplo de codigo a integrar en la clase PaymentScreen
    mediante herencia protoype
    Se debe integrar junto con el codigo completo del metodo _isOrderValid
    debe recibir el parametro (isForceValidate)
..........................................................................

odoo.define("pos_customer_required.PayScreen", function(require) {
    "use strict";

    const screens = require("point_of_sale.PaymentScreen");
    const core = require("web.core");
    const _t = core._t;



    screens.prototype._isOrderValid = async function(isForceValidate){
        
                    if ((this.env.pos.config.require_customer != "no" || this.currentOrder.is_paid()) && !this.currentOrder.get_client()) {
                        const { confirmed } = await this.showPopup('ConfirmPopup', {
                            title: this.env._t('Please select the Customer'),
                            body: this.env._t(
                                'You need to select the customer before you can invoice or ship an order.'
                            ),
                        });
                        if (confirmed) {
                            this.selectClient();
                        }
                        return false;
                    }
                   
                }


            return screens;
        });

    
................................................................................
*/
