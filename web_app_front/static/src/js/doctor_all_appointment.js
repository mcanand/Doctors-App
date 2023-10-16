odoo.define('web_app_front.doctor_all_appointment', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.doctor_all_appointment = publicWidget.Widget.extend({
        selector: '.doctor-all-appointment-container',
   events: {
            'click .left-button': '_onClickDoctorBox',
            'click .right-button': '_onClickPrescriptionBox',
        },

        start: function () {
            // Initially hide the "Previous" section
            $(".previous").hide();


            const upcomingButton = document.getElementById("upcoming-button");
            const previousButton = document.getElementById("previous-button");

            // Initial state: "Upcoming" button is active
            upcomingButton.classList.add("active-button");

            // Add click event listeners to toggle button classes
            upcomingButton.addEventListener("click", function () {
                upcomingButton.classList.add("active-button");
                previousButton.classList.remove("active-button");
            });

            previousButton.addEventListener("click", function () {
                previousButton.classList.add("active-button");
                upcomingButton.classList.remove("active-button");
            });
        },

        _onClickDoctorBox: function (ev) {
            // Handle click on the "Upcoming" button
            $(".upcoming").show();
            $(".previous").hide();
        },

        _onClickPrescriptionBox: function (ev) {
            // Handle click on the "Previous" button
            $(".upcoming").hide();
            $(".previous").show();
        },
    });
});
