odoo.define('web_app_front.rating', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.rating = publicWidget.Widget.extend({
        selector: '.doctor-rating-container',

        start: function () {
            this._super();
            // Add a click event listener to the "Rate Doctor" element
            this.$el.on('click', '.rating', this._onRateDoctor.bind(this));
        },

        _onRateDoctor: function (ev) {
            ev.preventDefault();
            var doctorId = $('#doctor_id').val();

            $('#ratingModal').modal('show');

            $('#submitRating').on('click', function () {
                var selectedRating = $('input[name="rate"]:checked').val();
                 var reviewText = $('#review').val();

                if (selectedRating !== undefined) {
                    // Send the selected rating to the server using AJAX
                    ajax.jsonRpc('/rate/doctor', 'call', { 'rating': selectedRating ,'id':doctorId,'review':reviewText})
                        .then(function (result) {
                            if (result.success) {
                                console.log("Rating submitted successfully.");
                                $('#ratingModal').modal('hide');
                            } else {
                                console.error("Error submitting rating:", result.message);
                            }
                        });
                } else {
                    console.error("Please select a rating before submitting.");
                }
            });
        },
    });
});
