odoo.define('web_app_front.doctor_information', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const {_t, qweb} = require('web.core');
    const session = require('web.session');

    publicWidget.registry.doctor_information = publicWidget.Widget.extend({
        events: {},
        init: function () {
            this._super.apply(this, arguments);
            var self = this;
            var modal = document.getElementById("myModal");
            var doctorBoxes = this.el.querySelectorAll(".doctor-box");

            doctorBoxes.forEach(function (doctorBox) {
                doctorBox.addEventListener("click", function () {
                    var doctorId = $(this).attr('data-id');
                    ajax.jsonRpc('/doctor/information/pick', 'call', {'doctor_id': doctorId})
                        .then(function (result) {
                            self.displayDoctorDetails(result); // Show the modal box with the returned data
                        });
                });
            });

            var span = document.getElementsByClassName("close")[0];
            window.onclick = function (event) {
                if (event.target === modal || event.target === span) {
                    modal.style.display = "none";
                }
            };
        },

        displayDoctorDetails: function (doctorDetails) {
            var modal = document.getElementById("myModal");
            var modalContent = document.querySelector(".modal-content p");
            modalContent.textContent = doctorDetails;
            modal.style.display = "block";

            // Close the modal when the user clicks the close button (x)
            var closeBtn = modal.querySelector(".close");
            closeBtn.onclick = function () {
                modal.style.display = "none";
            };

            // Close the modal when the user clicks outside the modal content
            window.onclick = function (event) {
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            };
        },
    });
});
