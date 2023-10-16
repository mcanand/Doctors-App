odoo.define('web_app_front.prescription', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.prescription = publicWidget.Widget.extend({
        selector: '.prescription-container',
        events: {
            'click .left': '_onClickDoctorBox',
            'click .right': '_onClickPrescriptionBox',
        },



        _onClickDoctorBox: function (ev) {
                     $(".case-details-box").show();
                $(".prescription-details-box").hide();
//            $(".case-details-box").html("<p>nn</p>");
        },

        _onClickPrescriptionBox: function (ev) {
                 $(".case-details-box").hide();
                $(".prescription-details-box").show();
//            $(".case-details-box").html("<p>mm</p>");
        },

    });
});
