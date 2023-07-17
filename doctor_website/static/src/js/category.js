odoo.define('doctor_website.category', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const {_t, qweb} = require('web.core');
    const session = require('web.session');

    publicWidget.registry.category = publicWidget.Widget.extend({
        selector: '.select_details',
        events: {
            'change select': '_onCategoryChange',
        },

        start: function () {
       alert('hhhhhhhhhhhh')
        },
//
      _onCategoryChange: function (ev) {
    // Handle the category change event here
            var v = $('#category_id :selected').attr('data-id');
            if (category_id) {
                ajax.jsonRpc('/doctor/get/slots', 'call', {'category_id': v})
                    .then(function (result) {
                        $.each(result, function (key, value) {
                            $('#slots').append("<option data-id='" + value.id + "'>" + value.name + "</option>")
                        });
                    });
            }
    },
    });
});
