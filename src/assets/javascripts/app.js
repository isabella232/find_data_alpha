!(function () {
  'use strict';

  var analytics = {
    init: function() {

      if (!window.ga) return;

      $('[data-ga-trigger]').on('click', function(event) {
        var action = $(event.target).data('ga-trigger');
        if (action) {
          var gaParams = [ 'send', 'event' ].concat(action.split(','));
          ga.apply(this, gaParams);
        }
      });
    }
  };

  $(document).ready(function() {
    analytics.init();
  });

})();
