odoo.define("pos_product_suggestion.models", function (require) {
    "use strict";

    const { PosGlobalState, Order, Orderline } = require('point_of_sale.models');
    const Registries = require("point_of_sale.Registries");
    
    const shSuggestionPosGlobalState = (PosGlobalState) => class shSuggestionPosGlobalState extends PosGlobalState {

        async _processData(loadedData) {
            var self = this
            self.suggestions = loadedData['product.suggestion'] || []

            self.suggestions = JSON.parse(JSON.stringify(self.suggestions))
            self.suggestion = {};
            _.each(self.suggestions, function (suggestion) {
                self.suggestion[suggestion.id] = suggestion;
            });
            
            await super._processData(...arguments);
        }
        
    }

    Registries.Model.extend(PosGlobalState, shSuggestionPosGlobalState);
});