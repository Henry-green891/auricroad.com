var $ = require('jquery');
import 'foundation-sites/dist/js/foundation.min.js';
import Player from '@vimeo/player';
import 'slick-carousel/slick/slick.min.js';

window.videoPlayer = null;
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
    setUpVideoSection();
    $(window).scroll(function(){
      setHeaderClass($(window).scrollTop());
      if (window.videoPlayer !== null && $(document).scrollTop() !== 0) {
        window.videoPlayer.getPaused().then(function(paused) {
          if (paused === false) {
            if($('#hero-video-iframe').hasClass('hide-on-load')) {
              $('#hero-video-iframe').hide();
            }
            window.videoPlayer.pause();
            $('.hero.video-only-hero .hero-video').removeClass('is-playing');
            $('#play-button-wrapper').removeClass('hidden');
            $('.desktop-nav-bar').removeClass('video-playing');
          }
        });
      }
    });
    $(window).resize(function(){
      setMobileDropdownState();
      clearTimeout(resizeTimer);
      var resizeTimer = setTimeout(function() {
        setVideoWidths();
      }, 250);
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

    // tabbed viewer code

    $('.slide-selector-tab').click(function(tab) {
      handleSlideSelectorTab(tab);
    });

    $('.slider').slick();

    // table clickable rows

    $('.clickable-row').click(function() {
        window.location = $(this).data('href');
    });

    $('.hero.video-only-hero video').each(function() {
      this.controls = false;
    });

    $('#play-button-wrapper').click(function() {
      if (window.videoPlayer !== null) {
        if($('#hero-video-iframe').hasClass('hide-on-load')) {
          $('#hero-video-iframe').show();
        }
        $(window).scrollTop(0);
        window.videoPlayer.play()
        $('.hero.video-only-hero .hero-video').addClass('is-playing');
        $('#play-button-wrapper').addClass('hidden');
        $('.desktop-nav-bar').addClass('video-playing');
      }
    });

    var options = {
      playsinline: false,
    }

    var iframe = $('#hero-video-iframe');
    if($('#hero-video-iframe').length > 0) {
      const player = new Player(iframe, options);
      window.videoPlayer = player;
      if(iframe.hasClass('hide-on-load')) {
        iframe.hide();
      }

      player.on('pause', function() {
        if($('#hero-video-iframe').hasClass('hide-on-load')) {
          $('#hero-video-iframe').hide();
        }
        $('.hero.video-only-hero .hero-video').removeClass('is-playing');
        $('#play-button-wrapper').removeClass('hidden');
        $('.desktop-nav-bar').removeClass('video-playing');
      });
    }
  }

  $(init);
})();

$(document).ready(function($) {

  $(document).foundation();
})


function setHeaderClass(scrollVal) {
  if (scrollVal > 16 || $('body').hasClass('only-scrolled-header')) {
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

function handleSlideSelectorTab(tab) {
  const itemId = tab.currentTarget.id;
  const itemIdNumber = filterNumberFromId(itemId, 'slide-selector-')
  $('.slide-selector-tab').removeClass('active-floorplan-tab-selector');
  $('#'+itemId).addClass('active-floorplan-tab-selector');
  $('.floor-plan-slide-wrapper').removeClass('active-floorplan-tab');
  $('#floor-plan-slide-wrapper-'+itemIdNumber+'').addClass('active-floorplan-tab');
  // reset gallery
  const slider = $('#floor-plan-slide-wrapper-'+itemIdNumber+'').find('.slider');
  slider[0].slick.refresh()
}

function generateVideoSize() {
  var width;
  if ($('body').hasClass('reduced-mobile-margins') && $(window).width() < 1024) {
   width = Math.round(((11 * $(window).width()) / 12) - 10);
  } else {
    width = Math.round(((5 * $(window).width()) / 6) - 10);
  }
  var height = Math.round((9 * width) / 16);
  return {
    width, height
  }
}

function setUpVideoSection() {
  var dimensions = generateVideoSize();
  $('.vimeo-video-wrapper').each(function() {
    var vimeoPlayer = new Player($(this));
    vimeoPlayer.on('loaded', function() {
      vimeoPlayer.element.height = dimensions.height;
      vimeoPlayer.element.width = dimensions.width;
    });
  });
}

function setVideoWidths() {
  var dimensions = generateVideoSize();
  $('.vimeo-video-wrapper iframe').each(function() {
    this.height = dimensions.height;
    this.width = dimensions.width;
  });
}

function filterNumberFromId(text, toRemove) {
  return text.replace(toRemove, '')

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
