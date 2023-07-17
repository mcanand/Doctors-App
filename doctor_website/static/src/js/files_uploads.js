odoo.define('doctor_website.files_uploads', function (require) {
    'use strict';
    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const {_t, qweb} = require('web.core');
    const session = require('web.session');
    console.log('kkkkkkkkkkkkkkk')

    publicWidget.registry.files_uploads = publicWidget.Widget.extend(
        selector: 'select_details',
        events:{},
        init: function () {
              alert('hhhhhhhhhhhh')

        },
        });
        });
//      $(document).ready(function() {
//      $('input[type="file"]').on('click', function() {
//      $(".file_names").html("");
//      })
//     if ($('input[type="file"]')[0]) {
//	  var fileInput = document.querySelector('label[for="et_pb_contact_brand_file_request_0"]');
//	  fileInput.ondragover = function() {
//		this.className = "et_pb_contact_form_label changed";
//		return false;
//	 }
//	fileInput.ondragleave = function() {
//		this.className = "et_pb_contact_form_label";
//		return false;
//	}
//	fileInput.ondrop = function(e) {
//		e.preventDefault();
//		var fileNames = e.dataTransfer.files;
//		for (var x = 0; x < fileNames.length; x++) {
//			console.log(fileNames[x].name);
//			$=jQuery.noConflict();
//			$('label[for="et_pb_contact_brand_file_request_0"]').append("<div class='file_names'>"+ fileNames[x].name +"</div>");
//		}
//	}
//	$('#et_pb_contact_brand_file_request_0').change(function() {
//		var fileNames = $('#et_pb_contact_brand_file_request_0')[0].files[0].name;
//		$('label[for="et_pb_contact_brand_file_request_0"]').append("<div class='file_names'>"+ fileNames +"</div>");
//		$('label[for="et_pb_contact_brand_file_request_0"]').css('background-color', '##eee9ff');
//	});
//	}
//});
