odoo.define('pos_multi_product_uom.productitem', function (require) {
	"use strict";
    
  const pos_model = require('point_of_sale.models');
  var exports = pos_model.Orderline;
  
  pos_model.Order = pos_model.Order.extend({
  

  add_product: function(product, options){
    
    if(this._printed){
        this.destroy();
        return this.pos.get_order().add_product(product, options);
    }
    this.assert_editable();
    options = options || {};
    var line = new pos_model.Orderline({}, {pos: this.pos, order: this, product: product});
    this.fix_tax_included_price(line);
    
    this.set_orderline_options(line, options);
    
    var to_merge_orderline;
    
    if("return" in options){
        line["uom_id"] = options.uom_id
    }
    

    for (var i = 0; i < this.orderlines.length; i++) {
        
        if (this.orderlines.models[i].uom_id === line.uom_id){
            if(this.orderlines.at(i).can_be_merged_with(line) && options.merge !== false){
                to_merge_orderline = this.orderlines.at(i);
        }
    }

    }
    if (to_merge_orderline){
        to_merge_orderline.merge(line);
        this.select_orderline(to_merge_orderline);
    } else {
        this.orderlines.add(line);
        this.select_orderline(this.get_last_orderline());
    }

    if (options.draftPackLotLines) {
        this.selected_orderline.setPackLotLines(options.draftPackLotLines);
    }
    if (this.pos.config.iface_customer_facing_display) {
        this.pos.send_current_order_to_customer_facing_display();
    }
    console.log("this.orderlines",this.orderlines);
},


  });
   
});
