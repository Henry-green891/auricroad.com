var $ = require('jquery');
import 'foundation-sites/dist/js/foundation.min.js';
(function() {
  function _makeExternal() {
    this.target = '_blank';
  }
  function _makeActive(){
    $(this).addClass('active');
  }
  function _isExternalLink() {
    var href = $(this).attr('href');
    return !(!href ||
             href[0] === '?' ||
             href[0] === '/' ||
             href[0] === '#' ||
             href.substring(0, 4) === 'tel:' ||
             href.substring(0, 7) === 'mailto:' ||
             href.substring(0, 11) === 'javascript:');
  }

  function _isCurrentPage(){
    var current_url = window.location.pathname;
    var href = $(this).attr('href');
    return (href == current_url);
  }

  function init() {
    $('a').filter(_isExternalLink).each(_makeExternal);
    $('.nav-link a').filter(_isCurrentPage).each(_makeActive);

    setHeaderClass($(window).scrollTop());
    setMobileDropdownState();
    $(window).scroll(function(){
      setHeaderClass($(window).scrollTop());
    });
    $(window).resize(function(){
      setMobileDropdownState();
    });
    $('.mobile-nav-top .left').click(function() {
      if($('.menu-btn').prop('checked')) {
        $('.menu-btn').prop('checked', false);
        $('.menu-dropdown').removeClass('expanded');
        $('.mobile-nav-top').removeClass('dropdown-expanded');
      } else {
        $('.menu-btn').prop('checked', true);
        $('.menu-dropdown').addClass('expanded');
        $('.mobile-nav-top').addClass('dropdown-expanded');
      }
    });

  }

  $(init);
})();

$(document).ready(function($) {

  $(document).foundation();
})


function setHeaderClass(scrollVal) {
  if (scrollVal > 16) {
    $('header .desktop-nav-bar').addClass('fixed');
  } else {
    $('header .desktop-nav-bar').removeClass('fixed');
  }
}

function setMobileDropdownState() {
  if ($(window).width() > 1024) {
    $('.menu-dropdown').removeClass('expanded');
    $('.menu-btn').prop('checked', false);
    $('.mobile-nav-top').removeClass('dropdown-expanded');
  }
}


function addToDict(dict, key, value) {
  key = encodeURIComponent(decodeURIComponent(key));
  value = encodeURIComponent(decodeURIComponent(value));
  dict[key] = value;
}

function addParamToSearch(param, value) {
  var params = {};
  location.search.substring(1).split('&').forEach(function(querystring) {
    if (querystring) {
      var split = querystring.split('=');
      addToDict(params, split[0], split[1]);
    }
  });
  addToDict(params, param, value);
  var queryString = '';
  for (var key in params) {
    var paramString = key + '=' + params[key];
    var separator = (queryString.indexOf('?') === -1) ? '?' : '&';
    queryString = queryString + separator + paramString;
  }
  return queryString;
}
addParamToSearch('', '')
