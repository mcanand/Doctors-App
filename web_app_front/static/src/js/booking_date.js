odoo.define('web_app_front.booking', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.booking = publicWidget.Widget.extend({
        selector: '.booking_container',
        events: {
            'click .booking': '_onClickDoctorBox',
            'click #add_date_btn': '_onClickPlusButton',
        },

        start: function () {

            this.hideSecondDateField(); // Hide the second date field initially
        },

        _onClickDoctorBox: function (ev) {
            var $button = $(ev.currentTarget);
            var firstDateValue = $("#next_sitting").val();
            if (firstDateValue !== "") {
                var firstDate = new Date(firstDateValue);
                var nextDate = new Date(firstDate.getTime() + 86400000);
                var nextDateString = nextDate.toISOString().split('T')[0];
                $("#next_sitting").val(nextDateString);
                this.showSecondDateField(); // Show the second date field on first click

            }
        },

        _onClickPlusButton: function (ev) {
            var $button = $(ev.currentTarget);
            var firstDateValue = $("#next_sitting").val();
            if (firstDateValue !== "") {
                var firstDate = new Date(firstDateValue);
                var nextDate = new Date(firstDate.getTime() + 86400000);
                var nextDateString = nextDate.toISOString().split('T')[0];
                this._addNewDateInput(nextDateString);

            }
        },

        _addNewDateInput: function (defaultValue) {
            var $dateInputsContainer = this.$('.date_inputs_container');
            var newInput = `<div class="form-group">
                                <label for="next_sitting_date">Next Sitting Date:</label>
                                <div class="input-group">
                                    <input type="date" class="form-control" name="next_sitting_date" value="${defaultValue || ''}" />
                                    <div class="input-group-append">
                                        <button type="button" class="btn btn-outline-secondary booking" id="add_date_btn">+</button>
                                    </div>
                                </div>
                            </div>
                              <div class="form-group" id="time">
                                <div class="input-group">
                                    <label for="from_time">From</label>
                                    <input type="time" class="form-control" name="from_time"/>
                                    <label for="to_time">To</label>
                                    <input type="time" class="form-control" name="to_time"/>
                                </div>
                            </div>`;
            $dateInputsContainer.append(newInput);
        },

        showSecondDateField: function () {
            var $secondDateField = this.$('#second_date_field');
            $secondDateField.removeClass('hidden');
        },

        hideSecondDateField: function () {
            var $secondDateField = this.$('#second_date_field');
            $secondDateField.addClass('hidden');
        },
    });
});
