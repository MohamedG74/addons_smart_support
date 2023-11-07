odoo.define('pos_all_in_one.LoyaltyButtonWidgetNew', function(require) {
	"use strict";

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

	class LoyaltyButton extends PosComponent {
		setup() {
            super.setup();
            useListener('click', this.onClick);
        }
		async onClick() {
			let order = this.env.pos.get_order();
			let self = this;
			let partner = false;
			let loyalty_points = 0;
			if(order.orderlines.length>0)
			{
				if(this.env.pos.pos_loyalty_setting.length != 0)
				{
					if (order.get_partner() != null){
						await self.env.pos._loadPartners([order.get_partner().id]);
						partner = order.get_partner();
						loyalty_points = partner.loyalty_points;
					}
										
					if(order.redeem_done){
						this.showPopup('ErrorPopup',{
							'title': this.env._t('استبدال النقاط'),
							'body': this.env._t('تم استبدال النقاط فى هذا الطلب من قبل.'),
						}); 
					}
					else if(this.env.pos.pos_loyalty_setting[0].redeem_ids.length == 0)
					{
						this.showPopup('ErrorPopup', {
							'title': this.env._t('تحذير'),
							'body': this.env._t('برجاء اعداد طريقة خصم النقاط'),
						}); 
					}
					else if(!partner){
						this.showPopup('ErrorPopup', {
							'title': this.env._t('عميل غير محدد'),
							'body': this.env._t('يجب تحديد عميل قبل الاستبدال'),
						});
					}
					else if(loyalty_points < 1){
						this.showPopup('ErrorPopup', {
							'title': this.env._t('لا يوجد نقاط'),
							'body': this.env._t('لا توجد نقاط كافية للاستبدال.'),
						});
					}
					else{
						this.showPopup('LoyaltyPopupWidget', {'partner':partner});
					} 
				}    
			}
			else{
				this.showPopup('ErrorPopup', {
					'title': this.env._t('طلب فارغ'),
					'body': this.env._t('برجائ اضافة الطلب قبل البدء فى الاسترداد'),
				}); 
			}		  
		}
	}
	LoyaltyButton.template = 'LoyaltyButton';

	ProductScreen.addControlButton({
		component: LoyaltyButton,
		condition: function() {
			return this.env.pos.pos_loyalty_setting.length > 0;
		},
	});

	Registries.Component.add(LoyaltyButton);

	return LoyaltyButton;

});
