/** @odoo-module **/
import { registry } from "@web/core/registry";
import { useInputField } from "@web/views/fields/input_field_hook";
import time from 'web.time';
var translation = require('web.translation');
var _t = translation._t;

const { Component,useRef} = owl;

export class DomainSelectorTextField extends Component {
    static template = 'FieldDateMultipleDate'

    setup(){
        super.setup();
        this.input = useRef('inputdate')
        useInputField({ getValue: () => this.props.value || "", refName: "inputdate" });
    }
    _onSelectDateField(ev){

        // this.props.update(this.input.el.value);

    //     var dateFormat = time.getLangDateFormat();
    //     console.log("dateFormat....",dateFormat);
    //    if (dateFormat.includes('MMMM')){
    //       var dates = dateFormat.toLowerCase()
    //       var result = dates.replace(/mmmm/g, 'MM');
    //       console.log("Result..............",result)
    //       dateFormat = result
    //   }
    //   else if (dateFormat.includes('MMM')) {
    //       var dates = dateFormat.toLowerCase()
    //       var result = dates.replace(/mmm/g, 'M');
    //       dateFormat = result
    //       console('date',result)

    //   }
    //   else if(dateFormat.includes('ddd')){
    //       var dates =new dateFormat.toLowerCase()
    //       var result = new dates.replace(/ddd/g, 'DD');
    //       console.log("Result..............",result)
    //       dateFormat = result
    //   }
    //  else{
    //     dateFormat = dateFormat.toLowerCase()
    //  }
          if (this.input.el){

            this.props.update(this.input.el.value);
            $(this.input.el).hijriDatePicker({
                locale: "ar-sa",
                format: "DD-MM-YYYY",
                hijriFormat:"iYYYY-iMM-iDD",
                dayViewHeaderFormat: "MMMM YYYY",
                hijriDayViewHeaderFormat: "iMMMM iYYYY",
                showSwitcher: false,
                allowInputToggle: true,
                showTodayButton: false,
                useCurrent: true,
                isRTL: true,
                viewMode:'months',
                keepOpen: true,
                hijri: true,
                debug: false,
                showClear: true,
                showTodayButton: true,
                showClose: true,
            }).trigger('focus');
    //         console.log('this',dateFormat)
    //         $(this.input.el).datepicker({
    //             multidate: true,
    //             format: dateFormat,
    //         }).trigger('focus');
         }
     }
}
registry.category("fields").add("multiple_datepicker", DomainSelectorTextField);
