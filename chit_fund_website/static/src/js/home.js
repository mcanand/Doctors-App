odoo.define('chit_fund_website.home', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var ajax = require('web.ajax');
    var _t = require('web.core');

    publicWidget.registry.home = publicWidget.Widget.extend({
        selector: '.carousel-container',


        start: function () {
            alert('hhh')
//            var self = this;
//            this._super.apply(this, arguments);
//            $(".carousel").swipe({
//                swipe: function (event, direction, distance, duration, fingerCount, fingerData) {
//                    if (direction === 'left') {
//                        $(this).carousel('next');
//                    }
//                    if (direction === 'right') {
//                        $(this).carousel('prev');
//                    }
//                },
//                allowPageScroll: 'vertical'
//            });
        },


    });
});
