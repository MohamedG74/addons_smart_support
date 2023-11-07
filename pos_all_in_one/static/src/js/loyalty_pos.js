odoo.define("pos_all_in_one.loyalty_pos", function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var PosDB = require('point_of_sale.DB');
	let utils = require('web.utils');

    // Load Models
	/*models.load_models({
		model: 'pos.loyalty.setting',
		fields: ['name', 'product_id', 'issue_date', 'expiry_date', 'loyalty_basis_on', 'loyality_amount', 'active','redeem_ids'],
		domain: function(self) {
			let today = new Date();
			let dd = today.getDate();
			let mm = today.getMonth()+1; //January is 0!

			let yyyy = today.getFullYear();
			if(dd<10){
				dd='0'+dd;
			} 
			if(mm<10){
				mm='0'+mm;
			} 
			today = yyyy+'-'+mm+'-'+dd;
			return [['company_id', '=', self.company && self.company.id || false],['issue_date', '<=',today],['expiry_date', '>=',today],['active','=',true]];
		},
		loaded: function(self, pos_loyalty_setting) {
			self.pos_loyalty_setting = pos_loyalty_setting;
		},
	});

	models.load_models({
		model: 'pos.redeem.rule',
		fields: ['reward_amt','min_amt','max_amt','loyality_id'],
        domain: function(self) {return [['company_id', '=', self.company && self.company.id || false]]},
		loaded: function(self, pos_redeem_rule) {
			self.pos_redeem_rule = pos_redeem_rule;
		},
	});

	models.load_fields('pos.category', ['Minimum_amount']);
	models.load_fields('res.partner', ['loyalty_points','loyalty_amount']);
	*/
	
	
    const shPosLoya = (PosGlobalState) => class shPosLoya extends PosGlobalState {

        async _processData(loadedData) {
            await super._processData(...arguments);
            this.pos_loyalty_setting = loadedData['pos_loyalty_setting'] || [];
            this.pos_redeem_rule = loadedData['pos_redeem_rule'] || [];
        }
        
    }

    Registries.Model.extend(PosGlobalState, shPosLoya);

    const shPosOrderLoyality = (Order) => class shPosOrderLoyality extends Order {
        constructor(attr, options) {
            super(...arguments);
            if (options && options.json && (options.json.loyalty)) {
                this.loyalty = options.json.loyalty;
            } else {
                this.loyalty = 0;
            }
            
            if (options && options.json && (options.json.redeemed_points)) {
                this.redeemed_points = options.json.redeemed_points;
            } else {
                this.redeemed_points = 0;
            }
            
            if (options && options.json && (options.json.redeem_done)) {
                this.redeem_done = options.json.redeem_done;
            } else {
                this.redeem_done = false;
            }
        }

        init_from_JSON (json) {
           
            super.init_from_JSON(...arguments);
            if (json && json.loyalty){
                this.loyalty = json.loyalty || ""
            }
            if (json && json.redeem_done){
                this.redeem_done = json.redeem_done || ""
            }
            if (json && json.redeemed_points){
                this.redeemed_points = json.redeemed_points || ""
            }
        }

        get_redeemed_points () {
            return parseInt(this.redeemed_points);
        }
        get_total_loyalty  () {
			let round_pr = utils.round_precision;
			let round_di = utils.round_decimals;
			let rounding = this.pos.currency.rounding;
			let final_loyalty = 0
			var order = this;
			let orderlines = order.get_orderlines();
			let partner_id = this.get_partner();

			if(this.pos.pos_loyalty_setting.length != 0)
			{	
			   if (this.pos.pos_loyalty_setting[0].loyalty_basis_on == 'pos_category') {
					if (partner_id)
					{
						let loyalty = 0
						for (let i = 0; i < orderlines.length; i++) {
							let lines = orderlines[i];
							let cat_ids = this.pos.db.get_category_by_id(lines.product.pos_categ_id[0])
							if(cat_ids){
								if (cat_ids['Minimum_amount']>0)
								{
									final_loyalty += parseInt(lines.get_price_with_tax() / cat_ids['Minimum_amount']);
								}
							}
						}
						return Math.floor(final_loyalty);
					}
			   }else if (this.pos.pos_loyalty_setting[0].loyalty_basis_on == 'amount') {
					let loyalty_total = 0
					if (order && partner_id)
					{
						let amount_total = order.get_total_with_tax();
						let subtotal = order.get_total_without_tax();
						let loyaly_points = this.pos.pos_loyalty_setting[0].loyality_amount;
						final_loyalty += (amount_total / loyaly_points);
						loyalty_total = order.get_partner().loyalty_points + final_loyalty;
						return Math.floor(final_loyalty);
					}
				}
			}
			return Math.floor(final_loyalty);
        }

        export_as_JSON () {
            const json = super.export_as_JSON(...arguments);
			json.redeemed_points = parseInt(this.redeemed_points);
			json.loyalty = this.get_total_loyalty();
			json.redeem_done = this.redeem_done || false;
			return json;
        }

    

    }

    Registries.Model.extend(Order, shPosOrderLoyality);

});
