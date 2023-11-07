// /** @odoo-module **/
// import { registry } from "@web/core/registry";
// import { useInputField } from "@web/views/fields/input_field_hook";
// import time from 'web.time';
// var translation = require('web.translation');
// var _t = translation._t;
// const { Component,useRef} = owl;
// export class DomainSelectorTextField extends Component {
//    static template = 'FieldDateMultipleDate'
//    setup(){
//        super.setup();
//        this.input = useRef('inputdate')
//        useInputField({ getValue: () => this.props.value || "", refName: "inputdate" });
//    }
//    _onSelectDateField(ev){
//        var dateFormat = time.getLangDateFormat();
//       if (dateFormat.includes('MMMM')){
//          var dates = dateFormat.toLowerCase()
//          var result = dates.replace(/mmmm/g, 'MM');
//          dateFormat = result
//      }
//      else if (dateFormat.includes('MMM')) {
//          var dates = dateFormat.toLowerCase()
//          var result = dates.replace(/mmm/g, 'M');
//          dateFormat = result
//      }
//      else if(dateFormat.includes('ddd')){
//          var dates =new dateFormat.toLowerCase()
//          var result = new dates.replace(/ddd/g, 'DD');
//          dateFormat = result
//      }
//     else{
//        dateFormat = dateFormat.toLowerCase()
//     }
//        if (this.input.el){
//           this.props.update(this.input.el.value.replace(DomainSelectorTextField, ''));
//            console.log('this',dateFormat)
//            $(this.input.el).datepicker({
//             multidate: true,
//             format: dateFormat,
//         }).trigger('focus');
//        }
//    }
// }
// registry.category("fields").add("multiple_datepicker", DomainSelectorTextField);
odoo.define('creating_widget.multiple_datepicker', function (require) {
    "use strict";
    
    var FieldRegistry = require('web.field_registry');
    var FieldChar = require('web.basic_fields').FieldChar;
    
    var FormDescriptionPage = FieldChar.extend({
    
        //--------------------------------------------------------------------------
        // Widget API
        //--------------------------------------------------------------------------
    
        /**
         * @private
         * @override
         */
        _renderEdit: function () {
            var def = this._super.apply(this, arguments);
            this.$el.addClass('col');
            var $inputGroup = $('<div class="input-group">');
            this.$el = $inputGroup.append(this.$el);
            var $button = $(`
                <button type="button" title="Open section" class="btn oe_edit_only o_icon_button">
                    <i class="fa fa-fw o_button_icon fa-external-link"/>
                </button>
            `);
            this.$el = this.$el.append($button);
            $button.on('click', this._onClickEdit.bind(this));
    
            return def;
        },
    
        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------
    
        /**
         * @private
         */
        _onClickEdit: function (ev) {
            ev.stopPropagation();
            var id = this.record.id;
            if (id) {
                this.trigger_up('open_record', {id: id, target: ev.target});
            }
        },
    });
    
    FieldRegistry.add('multiple_datepicker', FormDescriptionPage);
    
    });
    