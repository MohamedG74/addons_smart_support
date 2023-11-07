/**@odoo-module */

import Registries from "point_of_sale.Registries"
import ProductScreen from "point_of_sale.ProductScreen"
import models from "point_of_sale.models"

const ProductScreenInherit=(product_screen) => class extends product_screen{

    setup(){
        super.setup();
       
    }
    getCount() {
        const order = this.env.pos.get_order();
        const line_count = order ? order.get_orderlines().length : 0;
        let hasDiscount = false;
    
        for (const orderLine of order.get_orderlines()) {
            if (orderLine.product.id ==this.env.pos.config.discount_product_id[0]) {
                hasDiscount=true;
                break;
            }
        }
    
        if (hasDiscount) {
            return line_count - 1;
        } else {
            return line_count;
        }
    }
  
    
    
}

Registries.Component.extend(ProductScreen,ProductScreenInherit)