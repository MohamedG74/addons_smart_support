odoo.define("sh_pos_multi_barcode.models", function (require) {
    "use strict";

    const { PosGlobalState } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const shPosmultibarcodePoModel = (PosGlobalState) => class shPosmultibarcodePoModel extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments)
            var self = this
            self.db.multi_barcode_by_id = loadedData['product_by_barcode'] || {}
            if (self.config.sh_enable_multi_barcode){
                
                _.each(loadedData['product_by_barcode'], function (barcode) {
                    if (barcode.product_id){
                        self.db.product_by_barcode[barcode.name] = self.db.get_product_by_id(barcode.product_id)
                        if(self.db.product_by_id[barcode.product_id]['multi_barcodes']){
                            self.db.product_by_id[barcode.product_id]['multi_barcodes'] += '|' + barcode.name
                        }else{
                            self.db.product_by_id[barcode.product_id]['multi_barcodes'] = barcode.name
                        }
                    }
                })
            }
        }
    }
    Registries.Model.extend(PosGlobalState, shPosmultibarcodePoModel);

});
