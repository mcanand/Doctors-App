odoo.define('web_app_front.doctor_information_data', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.doctor_information_data = publicWidget.Widget.extend({
        selector: '.information-data-container',
        events: {
            'click .doctor-all-data': '_onClickDoctorBox',
        },

        start: function () {
//        alert('jj')
            this._super.apply(this, arguments);
            var self = this;
            var modal = document.getElementById("myModal");
            var span = document.getElementsByClassName("close")[0];

            // Close the modal when the user clicks the close button (x)
            span.onclick = function () {
                modal.style.display = "none";
            };

            // Close the modal when the user clicks outside the modal content
            window.onclick = function (event) {
                if (event.target === modal) {
                    modal.style.display = "none";
                }
            };
        },

        _onClickDoctorBox: function (ev) {
          var self = this;
             var doctorId = ev.currentTarget.getAttribute('data-id');
//             alert(doctorId)
            ajax.jsonRpc('/doctor/information/pick', 'call', {'doctor_id': doctorId})
                .then(function (result) {
                    self.displayDoctorDetails(result.data);
                });
        },

    displayDoctorDetails: function (doctorDetails) {
            var modal = document.getElementById("myModal");
            var modalDoctorName = modal.querySelector("#doctorName");
            var modalDoctorDepartment = modal.querySelector("#doctorDepartment");
            var modalDoctorImage = modal.querySelector("#doctorImage");
            var modalDoctorExperience = modal.querySelector("#doctorExperience");
            var modalDoctorAbout = modal.querySelector("#doctorAbout");
             var modalDoctorAboutFull = modal.querySelector("#doctorAboutFull");
            var modalDoctorRating = modal.querySelector("#doctorRating");
            var modalDoctorId = modal.querySelector("#doctorId");
            var modalScheduleMeetingButton = modal.querySelector("#myButton");

            modalDoctorName.textContent = doctorDetails.doctor_name;
            modalDoctorDepartment.textContent = doctorDetails.department_name;
            modalDoctorImage.querySelector("img").setAttribute("src", "data:image/png;base64," + doctorDetails.image);
            modalDoctorExperience.textContent = doctorDetails.experience + " Years of experience";
//            modalDoctorAbout.textContent = doctorDetails.about.substr(0, 100) + '...'; // Display truncated content
//            modalDoctorAboutFull.textContent = doctorDetails.about;
            if (typeof doctorDetails.about === 'string') {
                modalDoctorAbout.textContent = doctorDetails.about.substr(0, 100) + '...';
                modalDoctorAboutFull.textContent = doctorDetails.about;
            } else {
        // Handle the case where about is not a string
                 modalDoctorAbout.textContent = "About information not available";
                 modalDoctorAboutFull.textContent = "About information not available";
        }

            modalDoctorId.textContent = doctorDetails.doctor_id;
            modalDoctorRating.textContent = "Rating: " + doctorDetails.rating;
            modalScheduleMeetingButton.setAttribute("href", "/booking/availability/" + doctorDetails.doctor_id);
            var readMoreLink = modal.querySelector("#readMoreLink");
            if (readMoreLink) {
        // Toggle function for "Read More"
              var isExpanded = false;

            function toggleAboutContent() {
             if (isExpanded) {
                modalDoctorAbout.style.display = "block";
                modalDoctorAboutFull.style.display = "none";
                readMoreLink.innerText = "Read More...";
             } else {
                modalDoctorAbout.style.display = "none";
                modalDoctorAboutFull.style.display = "inline";
                readMoreLink.innerText = "Read Less";
             }
            isExpanded = !isExpanded;
           }

          readMoreLink.addEventListener("click", function (event) {
            event.preventDefault();
            toggleAboutContent();
        });
    }
            modal.style.display = "block";

        },
    });
});








