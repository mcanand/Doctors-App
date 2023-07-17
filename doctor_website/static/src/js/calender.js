odoo.define('doctor_website.calender', function (require) {
    'use strict';


    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const {_t, qweb} = require('web.core');
    const session = require('web.session');
    publicWidget.registry.calender = publicWidget.Widget.extend({

      start: function () {
          alert('hhhhhhhhhh')
         },

      function showHistory(historyId) {
        $.ajax({
            type: 'POST',
            url: '/get/history',
            data: JSON.stringify({'history_id': historyId}),
            contentType: 'application/json',
            success: function (data) {
                $('#divchange').html(data);
            }
        });
    }


});
});