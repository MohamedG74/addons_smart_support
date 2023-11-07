odoo.define('creating_widget.hijri_date_picker', function (require) {
    'use strict';

    var core = require('web.core');
    var FieldDate = require('web.basic_fields').FieldDate;

    var HijriDatePicker = FieldDate.extend({
        widget_class: 'o_hijri_datepicker',
        events: _.extend({}, FieldDate.prototype.events, {
            'changeDate': '_onDateChange',
        }),

        start: function () {
            this.$input = this.$('input.o_datepicker_input');
            this._super.apply(this, arguments);
        },

        _onDateChange: function () {
            var value = this.$input.val();
            if (value !== null) {
                this._setValue(this._parseDate(value));
            }
        },

        _renderEdit: function () {
            this._super.apply(this, arguments);
            this.$input.hijriDatePicker({
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
                keepOpen: false,
                hijri: true,
                debug: false,
                showClear: true,
                showTodayButton: true,
                showClose: true
            });
        },
    });

    core.form_widget_registry.add('hijri_date_picker', HijriDatePicker);

    return {
        HijriDatePicker: HijriDatePicker,
    };
});