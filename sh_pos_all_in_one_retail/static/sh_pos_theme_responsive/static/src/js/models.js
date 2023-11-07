odoo.define("sh_pos_theme_responsive.models", function (require) {

    var { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');


    const ShPosThemeSettingdPosGlobalState = (PosGlobalState) => class ShPosThemeSettingdPosGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.pos_theme_settings_data = loadedData['sh.pos.theme.settings'] || [];
            this.pos_theme_settings_data_by_theme_id = loadedData['pos_theme_settings_data_by_theme_id'] || [];
        }
        async after_load_server_data() {
            await super.after_load_server_data(...arguments);
            if (this.config.module_sh_pos_theme_settings) {
                this.hasLoggedIn = !this.config.module_sh_pos_theme_settings;
            }
        }
        get_cashier_user_id() {
            return this.user.id || false;
        }
    }

    Registries.Model.extend(PosGlobalState, ShPosThemeSettingdPosGlobalState);


});
