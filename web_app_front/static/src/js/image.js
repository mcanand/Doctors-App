odoo.define('web_app_front.image_det', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    var core = require('web.core');
    var ajax = require('web.ajax');
    var _t = core._t;

    publicWidget.registry.image_det = publicWidget.Widget.extend({
        selector: '.image_container',
          events:
       {
         'change input[type="file"]': '_onImageChange',

       },

        start: function () {
//            alert('Widget initialized.');

        },
         _onImageChange: function (ev)
    {
      var fileInput = document.getElementById('image_1920').files[0];
      var file = ev.target.files[0];
      var reader = new FileReader();
      reader.onload = function (e) {
      var imageSrc = e.target.result;
      var uploadedImage = document.querySelector('.uploaded-image.image_1920')
      uploadedImage.src = imageSrc;
    }
    reader.readAsDataURL(file);
 },

    });
});
