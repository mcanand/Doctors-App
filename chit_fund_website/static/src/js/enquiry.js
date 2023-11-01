odoo.define('chit_fund_website.enquiry', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var _t = require('web.core');

    publicWidget.registry.enquiry = publicWidget.Widget.extend({
        selector: '.check-container',

        start: function () {
//        alert('kkkk')
            this._super.apply(this, arguments);

            var self = this;

            // Function to open the modal
            function openModal() {
                var modal = document.getElementById("myModal");
                modal.style.display = "block";
            }

            // Function to close the modal
            function closeModal() {
                var modal = document.getElementById("myModal");
                modal.style.display = "none";
            }

            // Add an event handler to open the modal when the "Enquiry" button is clicked
            this.$el.on("click", "#open-modal-button", function (e) {
                e.preventDefault();
                openModal();
            });

            // Close the modal when the close button or outside the modal is clicked
            var modal = document.getElementById("myModal");
            var span = document.getElementsByClassName("close")[0];
            span.onclick = function () {
                closeModal();
            };
            window.onclick = function (event) {
                if (event.target === modal) {
                    closeModal();
                }
            };


        },
    });
});
