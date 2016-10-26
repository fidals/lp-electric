const autocomplete = function() {
  const config = {
    url: '/search/autocomplete/',
    searchInput: '.js-search-input',
    minChars: 2,
    itemsTypes: ['see_all', 'category', 'product'],
  };

  const init = () => {
    new autoComplete(constructorArgs);
  };

  /**
   * Constructor args for autocomplete lib
   * https://goodies.pixabay.com/javascript/auto-complete/demo.html
   */
  var constructorArgs = {
    selector: config.searchInput,
    minChars: config.minChars,
    source: function(term, response) {
      $.getJSON(config.url, {
        term
      }, function(namesArray) {
        response(namesArray);
      });
    },
  };

  init();
}();
