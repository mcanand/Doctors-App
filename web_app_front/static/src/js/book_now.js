odoo.define('web_app_front.book_now', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.book_now = publicWidget.Widget.extend({
        selector: '.user-container',
        events: {
            'click .user-box': '_onClickBookNow',
        },

        start: function () {
//            alert('j');
        },

        _onClickBookNow: function (ev) {
            var self = this;
            var slotId = ev.currentTarget.getAttribute('data-id');
            ajax.jsonRpc('/book/now', 'call', {'slot_id': slotId})
                .then(function (result) {
                    console.log(result);

                });
        },
    });
});
