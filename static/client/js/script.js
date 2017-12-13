  $('.navbar .menu').click(function () {
      $('body').toggleClass('active');
  });

  $(document).click(function () {
      if ($(window.event.target).attr('class') != '.search_outer')
          $("nav.navbar .search_outer").removeClass('active');
  });

  $("nav.navbar .search_outer input").on("click", function (e) {
      $(this).parent().toggleClass('active');
      e.stopPropagation();
  });
  $("nav.navbar .search_outer").on("click", function (e) {
      $(this).toggleClass('a');
      e.stopPropagation();
  });

  $('.sidebar.right .close').click(function () {
      $('body').toggleClass('open');

  });

  $('.dropdown').click(function () {
      $(this).toggleClass('active');
      $(this).parent().siblings().children('.dropdown') // get siblings of current elem
          .removeClass('active'); // remove class clicked from siblings
  });

  // Toggle Left Side //

  $(".menu").click(function () {
      $('.hamburger').toggleClass("open");
      if ($('body').hasClass("open")) {
          $('body').removeClass('open');
      }
  });


  (function ($) {

      //check if the browser width is less than or equal to the large dimension of an iPad
      if ($(window).width() >= 768) {

          // Toggle Right Side //

          $('#help').click(function () {
              $('body').removeClass('open');
              $('body').addClass('open');
              $('body').toggleClass('active');


              if ($('body').not(".active")) {
                  $('body').addClass('active');
              }

              if ($('.hamburger').hassClass("active")) {
                  $('.hamburger').removeClass('active');
              }

          });

          $('.sidebar.right .close').click(function () {
              $('body').toggleClass('active');
              $('body').removeClass('open');

              if ($('.hamburger').not(".open")) {
                  $('.hamburger').addClass('open');
              }

          });

      }
  })(jQuery);

  (function ($) {

      //check if the browser width is less than or equal to the large dimension of an iPad
      if ($(window).width() <= 767) {
          $('#help').click(function () {
              $('body').toggleClass('open');
          });

          $('.sidebar.right .close').click(function () {
              $('body').toggleClass('open');

          });

      }


  })(jQuery);

  $('.overlay').click(function () {
      $('body').removeClass('active');
      $('body').removeClass('open');
  });


  /*
  Reference: http://jsfiddle.net/BB3JK/47/
  */

  $('select').each(function () {
      var $this = $(this),
          numberOfOptions = $(this).children('option').length;

      $this.addClass('select-hidden');
      $this.wrap('<div class="select"></div>');
      $this.after('<div class="select-styled"></div>');

      var $styledSelect = $this.next('div.select-styled');
      $styledSelect.text($this.children('option').eq(0).text());

      var $list = $('<ul />', {
          'class': 'select-options'
      }).insertAfter($styledSelect);

      for (var i = 0; i < numberOfOptions; i++) {
          $('<li />', {
              text: $this.children('option').eq(i).text(),
              rel: $this.children('option').eq(i).val()
          }).appendTo($list);
      }

      var $listItems = $list.children('li');

      $styledSelect.click(function (e) {
          e.stopPropagation();
          $('div.select-styled.active').each(function () {
              $(this).removeClass('active').next('ul.select-options').hide();
          });
          $(this).toggleClass('active').next('ul.select-options').toggle();
      });

      $listItems.click(function (e) {
          e.stopPropagation();
          $styledSelect.text($(this).text()).removeClass('active');
          $this.val($(this).attr('rel'));
          $list.hide();
          //console.log($this.val());
      });

      $(document).click(function () {
          $styledSelect.removeClass('active');
          $list.hide();
      });

  });

  $('.nav-sidebar li a').on('click', function () {
      var target = $(this).attr('rel');
      $(".inner#" + target).toggleClass('active');
  });
  $('.nav-sidebar li a').click(function () {
      $('.nav-sidebar li').removeClass('active');
      $(this).parent().addClass('active');
      $('.inner').removeClass('active');
      $('.inner#' + $(this).attr('rel')).addClass('active');
  });
  $('.btn_show').click(function () {
      $('.nav-sidebar li').removeClass('active');
      $('.inner').removeClass('active');
      $('.inner#' + $(this).attr('rel')).addClass('active');
  });

  $('.btn_trigger').click(function () {
      $('.inner').removeClass('active');
      $('.inner#' + $(this).attr('rel')).addClass('active');
  });

  $('.right .edit').click(function () {
      $(this).parent().parent().find('.selected').removeClass('selected');
      $(this).parent().toggleClass('selected');
  });
  $('.right .close').click(function () {
      $(this).parent().parent().removeClass('selected');
  });
  $('.dropdown-menu.two li a').click(function () {
      $('.dropdown-menu.two li').removeClass('active');
      $(this).parent().addClass('active');
  })

  $('.hpeople .himg').click(function () {
      $(this).toggleClass('selected');
  });
  /* N4 Checkbox Script */
  $('.n4 input:checkbox').change(function () {
      if ($(this).is(":checked")) {
          $(this).parent().parent().addClass("selected");
      } else {
          $(this).parent().parent().removeClass("selected");
      }
  });
  /* Order Payment Select */
  $('.textfield .payment_method span').click(function () {
      $(this).parent().find('.selected').removeClass('selected');
      $(this).toggleClass('selected');
  });
  /*Payment Method */
  $('.textfield .payment_method .pf').click(function () {
      $('.payinfo').addClass('hidden');
      $('.payinfo#' + $(this).attr('rel')).removeClass('hidden');
  });

  /* Order Payment Select */
  $('.yorder .delete').click(function () {
      $(this).parent().addClass('deleted');
  });

  /* Billing Address Show/Hide */
  $('#trigger_baddress').click(function () {
      $('.textfield #baddress').toggleClass('active');
  });

  /* Show/Hide TOP Order Forms Widget */
  $('.ad .btn').click(function () {
      $('.order').addClass('display');
      $(this).parent().parent().addClass('active');
  });
  $('.ad .close').click(function () {
      $('.order').removeClass('display');
      $(this).parent().parent().removeClass('active');
  });
  $('.order .close').click(function () {
      $('.order').removeClass('display');
  });

  $('.btn_trigger').click(function () {
      $('.step').addClass('hidden');
      $('.step#' + $(this).attr('rel')).removeClass('hidden');
  });
  /* Show/Hide Order Item Inner */
  $('.list_item .list_top').click(function () {
      $(this).parent().toggleClass('active');
  });

  $('.profile .textfield .btn, .profile .addrinfo .btn, .profile .textfield .close').click(function () {
      $('.profile .textfield').toggleClass('active');
      $('.profile .addrinfo .btn').toggleClass('hidden');
  });


  $('.trigger_edit').click(function () {
      $('.worksheet#' + $(this).attr('rel')).toggleClass('active');
      $('.trigger_content').toggleClass('active');
  });

  $('.square.view').click(function () {
      $(this).parent().parent().toggleClass('active');
  });

  $('.square.viewa').click(function () {
      $(this).parent().parent().parent().parent().toggleClass('active');
      $('.it_outer').removeClass('active');
  });

  /* Body Click Trigger */