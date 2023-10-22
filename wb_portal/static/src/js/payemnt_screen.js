/**@odoo-module */

import Registries from "point_of_sale.Registries"
import PaymentScreen from "point_of_sale.PaymentScreen"

const PaymentScreenInherit=(payment_screen) => class extends payment_screen{

    setup(){
        super.setup();
        console.log("Hello gemy");
    }


    go_next(){
        console.log("Payment screen")
    }
}

Registries.Component.extend(PaymentScreen,PaymentScreenInherit)