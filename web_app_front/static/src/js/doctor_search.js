odoo.define('web_app_front.doctor_search', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.doctor_search = publicWidget.Widget.extend({
        selector: '.doctor-search-container',
        events: {
            'input .input-box input': '_onInputDoctorSearch',
        },

        start: function () {
            this._super();
//            alert('kkkk');
        },

        _onInputDoctorSearch: function (ev) {
            var searchTerm = $(ev.currentTarget).val().trim();
//            alert(searchTerm)
            if (searchTerm.length >= 2) { // You can adjust the minimum characters required
                this._fetchDoctorNames(searchTerm);
            }
        },

        _fetchDoctorNames: function (searchTerm) {
            var self = this;
            ajax.jsonRpc('/fetch/doctor/names', 'call', {search_term: searchTerm})
                .then(function (data) {

                     $('.row.mt-3').empty();


            $.each(data, function (key, value) {
                var doctorCard = '<div class="col-6 pb-3 text-center">' +
                                 '<a href="">' +
                                 '<div class="p-2 text-center align-self-center app_card">';

                if (value.image_1920) {
                    doctorCard += '<img class="doctor_image" src="data:image/png;base64,' + value.image_1920 + '"/>';
                } else {
                    doctorCard += '<svg class="doctor_image" xmlns="http://www.w3.org/2000/svg" height="2em" viewBox="0 0 384 512"><!-- SVG path definition here --></svg>';
                }

                doctorCard += '<p class="poppins400 mt-2" style="font-size:14px;">' + value.name + '</p>' +
                              '</div></a></div>';

                $('.row.mt-3').append(doctorCard);
            });
        });




        },


    });
});
