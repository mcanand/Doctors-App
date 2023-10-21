odoo.define('pos_custom_buttons.RecallButton', function(require) {
'use strict';
   const { Gui } = require('point_of_sale.Gui');
   const PosComponent = require('point_of_sale.PosComponent');
   const { posbus } = require('point_of_sale.utils');
   const ProductScreen = require('point_of_sale.ProductScreen');
   const { useListener } = require('web.custom_hooks');
   const Registries = require('point_of_sale.Registries');
   const PaymentScreen = require('point_of_sale.PaymentScreen');
   class RecallButton extends PosComponent {

   }
   RecallButton.template = 'RecallButton';
   ProductScreen.addControlButton({
        component: RecallButton,
        condition: function() {
            return this.env.pos;
        },
   });
   Registries.Component.add(RecallButton);
   return RecallButton;
});