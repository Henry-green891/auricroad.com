var $ = require('jquery');
import 'foundation-sites/dist/js/foundation.min.js';
import Player from '@vimeo/player';
import 'slick-carousel/slick/slick.min.js';
import datepickerFactory from 'jquery-datepicker';

window.videoPlayer = null;
(function () {
  function _makeExternal() {
    this.target = '_blank';
  }

  function _makeActive() {
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

  function _isCurrentPage() {
    var current_url = window.location.pathname;
    var href = $(this).attr('href');
    return href == current_url;
  }

  function init() {
    $('a').filter(_isExternalLink).each(_makeExternal);
    $('.nav-link a').filter(_isCurrentPage).each(_makeActive);

    setHeaderClass($(window).scrollTop());
    setMobileDropdownState();
    setUpVideoSection();
    $(window).scroll(function () {
      setHeaderClass($(window).scrollTop());
      if (window.videoPlayer !== null && $(document).scrollTop() !== 0) {
        window.videoPlayer.getPaused().then(function (paused) {
          if (paused === false) {
            if ($('#hero-video-iframe').hasClass('hide-on-load')) {
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
    $(window).resize(function () {
      setMobileDropdownState();
      clearTimeout(resizeTimer);
      var resizeTimer = setTimeout(function () {
        setVideoWidths();
      }, 250);
    });
    $('.mobile-nav-top .left').click(function () {
      if ($('.menu-btn').prop('checked')) {
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

    $('.slide-selector-tab').click(function (tab) {
      handleSlideSelectorTab(tab);
    });

    $('.slider').slick();

    // table clickable rows
    $('input[name*="date"]').datepicker();

    $('.clickable-row').click(function () {
      window.location = $(this).data('href');
    });

    $('.hero.video-only-hero video').each(function () {
      this.controls = false;
    });

    $('#play-button-wrapper').click(function () {
      if (window.videoPlayer !== null) {
        if ($('#hero-video-iframe').hasClass('hide-on-load')) {
          $('#hero-video-iframe').show();
        }
        $(window).scrollTop(0);
        window.videoPlayer.play();
        $('.hero.video-only-hero .hero-video').addClass('is-playing');
        $('#play-button-wrapper').addClass('hidden');
        $('.desktop-nav-bar').addClass('video-playing');
      }
    });

    var options = {
      playsinline: false,
    };

    var iframe = $('#hero-video-iframe');
    if ($('#hero-video-iframe').length > 0) {
      const player = new Player(iframe, options);
      window.videoPlayer = player;
      if (iframe.hasClass('hide-on-load')) {
        iframe.hide();
      }

      player.on('pause', function () {
        if ($('#hero-video-iframe').hasClass('hide-on-load')) {
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

$(document).ready(function ($) {
  $(document).foundation();
});

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
  const itemIdNumber = filterNumberFromId(itemId, 'slide-selector-');
  $('.slide-selector-tab').removeClass('active-floorplan-tab-selector');
  $('#' + itemId).addClass('active-floorplan-tab-selector');
  $('.floor-plan-slide-wrapper').removeClass('active-floorplan-tab');
  $('#floor-plan-slide-wrapper-' + itemIdNumber + '').addClass('active-floorplan-tab');
  // reset gallery
  const slider = $('#floor-plan-slide-wrapper-' + itemIdNumber + '').find('.slider');
  slider[0].slick.refresh()
}

function generateVideoSize() {
  var width;
  if ($('body').hasClass('reduced-mobile-margins') && $(window).width() < 1024) {
    width = Math.round(((11 * $(window).width()) / 12) - 10);
  } else {
    width = Math.round((5 * $(window).width()) / 6 - 10);
  }
  var height = Math.round((9 * width) / 16);
  return {
    width,
    height
  }
}

function setUpVideoSection() {
  var dimensions = generateVideoSize();
  $('.vimeo-video-wrapper').each(function () {
    var vimeoPlayer = new Player($(this));
    vimeoPlayer.on('loaded', function () {
      vimeoPlayer.element.height = dimensions.height;
      vimeoPlayer.element.width = dimensions.width;
    });
  });
}

function setVideoWidths() {
  var dimensions = generateVideoSize();
  $('.vimeo-video-wrapper iframe').each(function () {
    this.height = dimensions.height;
    this.width = dimensions.width;
  });
}

function filterNumberFromId(text, toRemove) {
  return text.replace(toRemove, '');
}

function addToDict(dict, key, value) {
  key = encodeURIComponent(decodeURIComponent(key));
  value = encodeURIComponent(decodeURIComponent(value));
  dict[key] = value;
}

function addParamToSearch(param, value) {
  var params = {};
  location.search.substring(1).split('&').forEach(function (querystring) {
    if (querystring) {
      var split = querystring.split('=');
      addToDict(params, split[0], split[1]);
    }
  });
  addToDict(params, param, value);
  var queryString = '';
  for (var key in params) {
    var paramString = key + '=' + params[key];
    var separator = queryString.indexOf('?') === -1 ? '?' : '&';
    queryString = queryString + separator + paramString;
  }
  return queryString;
}
addParamToSearch('', '')

// AUTOPOPULATE RESORT FUNCTION IN EVENTS FORM DROPDOWN FROM RESORT PAGE CLICKED FROM
let resort_pick = sessionStorage.getItem('resort_pick');

$(document).ready(function () {
  if (resort_pick == 'lmr') {
    $('#id_petite_resort').val('Lone Mountain Ranch (Big Sky MT)');
  } else if (resort_pick == 'ka') {
    $('#id_petite_resort').val('Korakia Pensione (Palm Springs CA)');
  } else if (resort_pick == 'hj') {
    $('#id_petite_resort').val('Hotel Joaquin (Laguna Beach CA)');
  } else if (resort_pick == 'sma') {
    $('#id_petite_resort').val('Sonoma Coast Villa (Sonoma Coast CA)');
  }
  // NOTE: stops negative numbers on number inputs via arrows (may not be needed since arrows are hidden and people can still type negative numbers in there)
  $('input[type="number"]').attr({
    'min': 0
  });
});

$(':button').click(function () {
  sessionStorage.setItem('resort_pick', '');
  if (this.className.includes('lone_mountain_ranch_events_form_link')) {
    sessionStorage.setItem('resort_pick', 'lmr');
  } else if (this.className.includes('korakia_events_form_link')) {
    sessionStorage.setItem('resort_pick', 'ka');
  } else if (this.className.includes('hotel_joaquin_events_form_link')) {
    sessionStorage.setItem('resort_pick', 'hj');
  } else if (this.className.includes('sonoma_events_form_link')) {
    sessionStorage.setItem('resort_pick', 'sma');
  }
});

// ADDS TRANSPORTATION DETAIL DROPDOWNS IF "Driving Myself" or "Need Transportation" IS SELECTED ON GUEST PROFILE FORM
$('input[id=id_transportation_1]').click(function () {
  $('.renting-car').css('display', 'block')
  $('.flight-details-header').css('display', 'none')
  $('.flight-details').css('display', 'none')
  $('.party-eta').css('display', 'block')
  $('input[id=id_arrival_location]').val('')
  $('input[id=id_arrival_flight_date]').val('')
  $('input[id=id_arrival_flight_time]').val('')
  $('input[id=id_arrival_airline]').val('')
  $('input[id=id_arrival_flight_number]').val('')
  $('input[id=id_departure_location]').val('')
  $('input[id=id_departure_flight_date]').val('')
  $('input[id=id_departure_flight_time]').val('')
  $('input[id=id_departure_airline]').val('')
  $('input[id=id_departure_flight_number]').val('')
})

$('input[id=id_transportation_0]').click(function () {
  $('.renting-car').css('display', 'none')
  $('.booked-car').css('display', 'none')
  $('.party-eta').css('display', 'none')
  $('input[id=id_party_eta]').val('')
  $('input[id=id_renting_car_0]').prop('checked', false)
  $('input[id=id_renting_car_1]').prop('checked', false)
  $('input[id=id_booked_car_0]').prop('checked', false)
  $('input[id=id_booked_car_1]').prop('checked', false)
  $('.flight-details-header').css('display', 'flex')
  $('.flight-details').css('display', 'flex')
})

$('input[id=id_renting_car_0]').click(function () {
  $('.booked-car').css('display', 'block')
})

$('input[id=id_renting_car_1]').click(function () {
  $('.booked-car').css('display', 'none')
  $('input[id=id_booked_car_0]').prop('checked', false)
  $('input[id=id_booked_car_1]').prop('checked', false)
});

// NOTE: rerenders selected option in the event of submission error
$(document).ready(function () {
  let number_selected_adults = $('#id_number_of_adults')[0].value;
  let number_selected_children = $('#id_number_of_children')[0].value;
  if (number_selected_adults > 0) {
    for (let i = 1; i <= number_selected_adults; i++) {
      let element_header = $('.party-details-header-adult-' + i)[0];
      let element = $('.party-details-adult-' + i)[0];
      element.style.display = 'flex';
      element_header.style.display = 'flex';
    }
  }
  if (number_selected_children > 0) {
    for (let i = 1; i <= number_selected_children; i++) {
      let element_header = $('.party-details-header-child-' + i)[0];
      let element = $('.party-details-child-' + i)[0];
      element.style.display = 'flex';
      element_header.style.display = 'flex';
    }
  }
});

// TODO: too much repeating code, needs refactor
$('#id_number_of_adults').change(function () {
  for (let i = 1; i <= 10; i++) {
    let element_header = $('.party-details-header-adult-' + i)[0];
    let element = $('.party-details-adult-' + i)[0];
    element.style.display = 'none';
    element_header.style.display = 'none';
  }
  let number_selected = $('#id_number_of_adults')[0].value;
  for (let i = 1; i <= number_selected; i++) {
    let element_header = $('.party-details-header-adult-' + i)[0];
    let element = $('.party-details-adult-' + i)[0];
    element.style.display = 'flex';
    element_header.style.display = 'flex';
  }
});

$('#id_number_of_children').change(function () {
  for (let i = 1; i <= 10; i++) {
    let element_header = $('.party-details-header-child-' + i)[0];
    let element = $('.party-details-child-' + i)[0];
    element.style.display = 'none';
    element_header.style.display = 'none';
  }
  let number_selected = $('#id_number_of_children')[0].value;
  for (let i = 1; i <= number_selected; i++) {
    let element_header = $('.party-details-header-child-' + i)[0];
    let element = $('.party-details-child-' + i)[0];
    element.style.display = 'flex';
    element_header.style.display = 'flex';
  }
});

datepickerFactory($);

$(function () {
  $('.datepicker-wrapper input').datepicker();
});

// AUTO-POPULATING EVENTS FORM
$(document).ready(function () {
  if (document.URL.includes('?resort=korakia')) {
    $('#id_petite_resort').val('Korakia Pensione (Palm Springs CA)');
    $('.event-form-things-to-know.korakia').css('display', 'block');
    if (document.URL.includes('&event=wedding')) {
      $('#id_event_type').val('Wedding Ceremony & Reception');
    }
  } else if (document.URL.includes('?resort=hoteljoaquin')) {
    $('#id_petite_resort').val('Hotel Joaquin (Laguna Beach CA)');
    $('.event-form-things-to-know.hotel-joaquin').css('display', 'block');
    if (document.URL.includes('&event=wedding')) {
      $('#id_event_type').val('Wedding Ceremony & Reception');
    } else if (document.URL.includes('&event=corporateretreat')) {
      $('#id_event_type').val('Corporate Retreat');
      $('.event-form-things-to-know.hotel-joaquin').css('display', 'none');
    } else if (document.URL.includes('&event=photoshoot')) {
      $('#id_event_type').val('Photoshoot');
    }
  } else if (document.URL.includes('?resort=lonemountainranch')) {
    $('#id_petite_resort').val('Lone Mountain Ranch (Big Sky MT)');
    $('.event-form-things-to-know.lone-mountain-ranch').css('display', 'block');
    // can't use wedding for now because all sub-event pages use the same template (event-individual-wide.php)
  } else if (document.URL.includes('?resort=sonoma')) {
    // no sonoma link to the events form yet, will need to add this to the link url when it's eventually created
    $('#id_petite_resort').val('Sonoma Coast Villa (Sonoma Coast CA)');
    $('.event-form-things-to-know.sonoma').css('display', 'block');
  }
});
