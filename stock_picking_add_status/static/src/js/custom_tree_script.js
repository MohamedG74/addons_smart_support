odoo.define('stock_picking_add_status.custom_tree_script', function (require) {
    'use strict';

    var ListController = require('web.ListController');
    var core = require('web.core');
    var qweb = core.qweb;

    ListController.include({
        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            var origin = this.renderer.state.data.parent.origin;
            if (origin === 'x') {
                this.$buttons.find('.o_list_button_add').hide();
            }
        },
    });
});