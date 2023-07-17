odoo.define('doctor_website.pagination', function (require) {
    'use strict';

    var publicWidget = require('web.public.widget');
    const Dialog = require('web.Dialog');
    const {_t, qweb} = require('web.core');
    const session = require('web.session');

    var PaginationWidget = publicWidget.Widget.extend({
        selector: '.select_details',

        start: function () {
            this._super();

            // Bind click events to the 'Previous' and 'Next' links
            this.$el.on('click', 'a[data-action="previous"]', this._onPreviousClick.bind(this));
            this.$el.on('click', 'a[data-action="next"]', this._onNextClick.bind(this));
        },

        _onPreviousClick: function (ev) {
            ev.preventDefault();

            var currentPage = parseInt($(ev.currentTarget).data('page'));
            var previousPage = currentPage - 1;

            if (previousPage >= 1) {
                // Retrieve the HTML template for the previous page
                this._getPageData(previousPage);

                // Update the URL with the new page number
                history.pushState(null, null, '/all/booking?page=' + previousPage);
            }
        },

        _onNextClick: function (ev) {
            ev.preventDefault();

            var currentPage = parseInt($(ev.currentTarget).data('page'));
            var nextPage = currentPage + 1;

            // Retrieve the HTML template for the next page
            this._getPageData(nextPage);

            // Update the URL with the new page number
            history.pushState(null, null, '/all/booking?page=' + nextPage);
        },

        _getPageData: function (pageNumber) {
            var self = this;

            $.get('/all/booking', { page: pageNumber }).done(function (data) {
                // Replace the table body with the updated HTML
                var tableBody = self.$el.closest('table').find('tbody');
                tableBody.html($(data).find('tbody').html());

                // Update the 'Previous' link with the new page number
                self.$el.find('a[data-action="previous"]').data('page', pageNumber);

                // Update the 'Next' link with the new page number
                self.$el.find('a[data-action="next"]').data('page', pageNumber + 1);

                // Update the current page number and page count in the summary
                self.$el.find('.oe_pager_summary').text('Page ' + pageNumber + ' of ' + data.page_count);

                // Enable/disable 'Previous' and 'Next' links based on page numbers
                self.$el.find('a[data-action="previous"]').prop('disabled', pageNumber === 1);
                self.$el.find('a[data-action="next"]').prop('disabled', pageNumber >= data.page_count);
            });
        },
    });

    return PaginationWidget;
});
