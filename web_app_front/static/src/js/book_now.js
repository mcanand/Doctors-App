odoo.define('web_app_front.book_now', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.book_now = publicWidget.Widget.extend({
        selector: '.details-container',
        events: {
            'click .detail-box': '_onClickBookNow',
        },
        _onClickBookNow: function (ev) {
            var self = this;
            var slotId = ev.currentTarget.getAttribute('data-id');
            ajax.jsonRpc('/book/now', 'call', {'slot_id': slotId})
                .then(function (result) {
                    if(result){
                        window.location.replace(result);
                    }
                    else{
                        console.log('update your address')
                    }
                });
        },
    });
});
