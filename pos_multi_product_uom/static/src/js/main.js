var ranPriceSet = false;
var globalunits = 0;
var s = false;
odoo.define('pos_multi_product_uom.main', function (require) {
	"use strict";
	var pos_model = require('point_of_sale.models');
  
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
  
  pos_model.load_fields('product.product','uom_ids');
  pos_model.Orderline=pos_model.Orderline.extend({
    init_from_JSON: function(json) {
      SuperOrderline.init_from_JSON.call(this,json);
      this.uom_id=json.uom_id;
    },
    get_unit: function(){
        var unit=SuperOrderline.get_unit.call(this);
        if(!this.uom_id){
          return unit;
        }
        var unit_id = this.uom_id;
        return this.pos.units_by_id[unit_id];
    },
    set_unit: function(unit){
      
      this.uom_id=unit;
      
      this.trigger('change', this);
    },
		set_unit_price: function(price){
      if(!this.price_manually_set){
        var new_price=(price*this.pos.units_by_id[this.product.uom_id[0]].factor)/this.get_unit().factor;
        
        SuperOrderline.set_unit_price.call(this,new_price);
      }else{
        SuperOrderline.set_unit_price.call(this,price);
      }
    },
    // set_unit_price: function(price){
      
    //   if(this.price_manually_set !== false){
        
          
    //     var new_price=(price*this.pos.units_by_id[this.product.uom_id[0]].factor_inv)/this.get_unit().factor;
    //     console.log("new_price",new_price);
    //     SuperOrderline.set_unit_price.call(this,new_price);
    //   }else{
    //     // console.log("else",price);
    //     SuperOrderline.set_unit_price.call(this,price);
    //   }
    // //   ranPriceSet=true;
    // this.trigger('change', this);

    // },
    export_as_JSON: function() {
      var pack_lot_ids = SuperOrderline.export_as_JSON.call(this);
      pack_lot_ids.uom_id=this.get_unit().id;
      
      return pack_lot_ids;
    },
  });

  // Unit Selection Popup----------------
  class UnitSelectionPopupWidget extends AbstractAwaitablePopup {
    constructor() {
        super(...arguments);
        var self = this;
        self.item='';
        self.value=''||self.props.value;
        self.props.is_selected = self.props.is_selected || false;
        self.list = self.props.list || [];
        for(var el in self.list){
            self.list[el].selected=false;
            if(self.list[el].item==self.value){
              self.list[el].selected=self;
            }
        }
        this.render();
    }
    click_item(event){
      var self = this;
      
      var item = this.props.list[parseInt($(event.target).data('item-index'))];
      item = item ? item.item : item;
      this.item=item;
      for(var el in this.props.list){
        this.props.list[el].selected=false;
      }
      this.props.list[parseInt($(event.target).data('item-index'))].selected=true;
      if(item==this.value){
        this.props.is_selected=false;
      }else{
        this.props.is_selected=true;
      }
      this.render();
    }
    
    
    click_confirm(event){
      var self = this;
      var l = self.props.orderline.models.length
      
      // var price=self.props.orderline.models[l-1].price*self.props.orderline.models[l-1].get_unit().factor/self.env.pos.units_by_id[self.item].factor;
      console.log(self.props.orderline.models);
      var price=self.props.orderline.models[l-1].price*self.env.pos.units_by_id[self.item].factor_inv;
      let globalunits = self.props.orderline.models[l-1].get_unit();

      self.props.orderline.models[l-1].price=price;
      
      
      self.props.orderline.models[l-1].set_unit(self.item);
      for(let i=0; i<self.list.length; i++){

        if(self.item === self.list[i]['item'] ){
            var v = self.list[i]['label']
            self.props.orderline.models[l-1].product.uom_id = [self.item,v];
          }
      }

      self.props.orderline.models[l-1].price_manually_set=true;
      ranPriceSet=true;
      
      NumberBuffer.reset();
      this.cancel();
    }     
  }
  UnitSelectionPopupWidget.template = 'UnitSelectionPopupWidget';
  UnitSelectionPopupWidget.defaultProps = {
      title: 'Confirm ?',
      value:''
  };
      Registries.Component.add(UnitSelectionPopupWidget)

      const ProductItempopup = (ProductScreen) =>

      class extends ProductScreen {
      constructor() {
      super(...arguments);

      }
      async _clickProduct(event){ 
          var self = this;
          var pro = event.detail;
          var categ = [];
          var ShouldPopUpShow=false;
          if (pro.uom_ids.length !== 0){
            if (!this.currentOrder) {
                  this.env.pos.add_new_order();
              }
              
              const product = event.detail;
              // console.log("this.currentOrder",product);
              
              var options = this._getAddProductOptions(product);
              // console.log("options",options);
              if (!options) return;
              this.currentOrder.add_product(product, options);
              
              
              NumberBuffer.reset();

    
                for(var index in pro.uom_ids){
                  var key = pro.uom_ids[index];
                 for (var vl in self.env.pos.units){
                  var unitobj=self.env.pos.units[vl];
                  if(unitobj.id==key){
                    categ.push({item:unitobj.id,label:unitobj.name,selected:false});
                    ShouldPopUpShow=true;}}}
                    if(ShouldPopUpShow){
                        self.showPopup('UnitSelectionPopupWidget', {
                          title: "Select Unit of Measure",
                          list: categ,
                          value:self.env.pos.units.id, 
                          orderline:this.currentOrder.orderlines
                        });
                      }
                      
                }
                else{
                  if (!this.currentOrder) {
                    this.env.pos.add_new_order();
                }
                
                const product = event.detail;
                var options = await this._getAddProductOptions(product);
                
                if (!options) return;
                
                this.currentOrder.add_product(product, options);
                NumberBuffer.reset();
                }
                  
              
            
              
              
          }
          
      };
  Registries.Component.extend(ProductScreen, ProductItempopup);
  
  return ProductScreen;

  

});