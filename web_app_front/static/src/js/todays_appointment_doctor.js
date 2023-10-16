odoo.define('web_app_front.todays_appointment_doctor', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var _t = core._t;

    publicWidget.registry.todays_appointment_doctor = publicWidget.Widget.extend({
        selector: '.doctor-appointment-container',
        events: {
            'click .left-button': '_onClickPersonal', // Updated to handle "Group" button
            'click .right-button': '_onClickGroup', // Updated to handle "Personal" button
        },

        start: function () {
            // Initially show the "Group" section and hide the "Personal" section
            $(".group-appointments").hide();
            $(".personal-appointments").show();
              const upcomingButton = document.getElementById("personal-button");
            const previousButton = document.getElementById("group-button");

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

        _onClickGroup: function (ev) {
            // Handle click on the "Group" button
            $(".group-appointments").show();
            $(".personal-appointments").hide();
        },

        _onClickPersonal: function (ev) {
            // Handle click on the "Personal" button
            $(".group-appointments").hide();
            $(".personal-appointments").show();
        },
    });
});
