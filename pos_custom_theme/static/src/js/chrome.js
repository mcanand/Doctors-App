odoo.define('pos_custom_theme.chrome', function (require) {
    'use strict';

    const Chrome = require('point_of_sale.Chrome');
    const Registries = require('point_of_sale.Registries');

    const PosThemeChrome = (Chrome) => class extends Chrome {
            _buildChrome() {
                super._buildChrome()
                this.state.theme = this.env.pos.config.themes
            }
        };

    Registries.Component.extend(Chrome, PosThemeChrome);

    return Chrome;
});
