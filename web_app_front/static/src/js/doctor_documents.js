odoo.define('web_app_front.documents_det', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.documents_det = publicWidget.Widget.extend({
        selector: '.documents_container',

        start: function () {
            var self = this;

            // Wait for DOMContentLoaded before attaching the event listener
            document.addEventListener("DOMContentLoaded", function () {
                var fileInput = document.getElementById("et_pb_contact_brand_file_request_0");

                fileInput.addEventListener("change", function (event) {
                    var selectedFiles = event.target.files;

                    for (var i = 0; i < selectedFiles.length; i++) {
                        console.log("Selected file:", selectedFiles[i].name);
                    }
                });
            });

            alert('Widget initialized.');

            // Call _super to invoke the parent class start method
            return this._super.apply(this, arguments);
        },
    });
});
