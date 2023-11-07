odoo.define('smart_pos_salesperson_emp.models', function(require){
    'use strict';
    var { PosGlobalState,Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    var core = require('web.core');
    var _t = core._t;
    //
    const newemPosGlobalState = (PosGlobalState) => class newemPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.employeenew = [];
            this.env.services.rpc({
                model: 'hr.employee',
                method: 'get_employee_sales_data',
                args: [],
            }).then((result) => {
                // result contains the HR employee data
                // you can use the data as needed in your Point of Sale module
                this.employeenew = result;
                this.employee_by_idn = [];
                result.forEach(obj => {
                    const {id, name, user_id} = obj;
                    this.employee_by_idn[id] = {id, name, user_id};
                });
            });
        }
    };

    Registries.Model.extend(PosGlobalState, newemPosGlobalState);
    const PosSaleOrderline = (Orderline) => class PosSaleOrderline extends Orderline {
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            if (json.user_id) {
                var user = this.get_user_by_id(json.user_id);
                if (user) {
                    this.set_line_user(user);
                }
            }
        }
        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            if (this.user_id) {
                json.user_id = this.user_id.id;
            }
            return json;
        }
        get_user_image_url () {
            if (this.user_id && this.user_id.id !== undefined) {
                return window.location.origin + '/web/image?model=hr.employee&field=image_128&id=' + this.user_id.id;
            }
            return null;
        }
        get_user_by_id (user_id) {
            var self = this;
            var user = null;
            for (var i = 0; i < self.pos.employeenew.length; i++) {
                if (self.pos.employeenew[i].id == user_id) {
                    user = self.pos.employeenew[i];
                }
            }
            return user;
        }
        get_line_user () {
            if (this.user_id && this.user_id.id !== undefined) {
                return this.user_id;
            }
            return null;
        }
        set_line_user (user) {
            this.user_id = user;
        }
        remove_sale_person () {
            this.user_id = null;
        }
    }
    Registries.Model.extend(Orderline, PosSaleOrderline);
});
