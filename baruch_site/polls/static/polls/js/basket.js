/**
*   Functions for cork buttons in the Home/Profile page
**/

$(document).ready(function () {

  addCorkToBasketModal();
  saveCorkToBasket();
  saveCorkToOtherBasket();
  editCorkForm();
  deleteCork();
  ajaxCorkToBasket();

})

$(window).load(function(){
   submenu(); 
});

function submenu() {
  jQuery('.submenu').hover(function () {
      jQuery(this).children('ul').removeClass('submenu-hide').addClass('submenu-show');
  }, function () {
      jQuery(this).children('ul').removeClass('.submenu-show').addClass('submenu-hide');
  }).find("a:first").append(" &raquo; ");
}

function addCorkToBasketModal() {

    // remove default cork field
    var default_field = $('#createBasketCorkModal').find('#id_corks');
    if (default_field.length > 1) {
      console.log("removing extra cork field");
      default_field = default_field[0];
      default_field = $(default_field).parents().eq(1);
      $(default_field).remove();
    }

  $('.newBasket').on('click', function() {
    var cork = $(this).attr('title');
    var row = $(this).attr('row');
    var data_target = $(this).attr('data-target');

    $(data_target).find('.modal-header div').attr('row', row);
    $(data_target).find('.modal-header div').text(cork);
    $(data_target).find('#id_corks option:first').val(row);
    $(data_target).find('#id_corks option:first').text(cork);
    $(data_target).modal('show');

    var basket_form = $(data_target).find('form');
    var submit_btn = $(data_target).find(':submit');

  });
}

function ajaxCorkToBasket() {
  basketModal('#createBasketCorkModal');
  $('#createBasketCorkModal :submit').on('click', function(ev) {
    var submit_btn = $(this);
    var basket_form = $('#createBasketCorkModal form');
    var data_target = '#createBasketCorkModal';

    ev.preventDefault();

    submit_btn.button('loading');
    basket_form.ajaxSubmit({
      complete: function(XMLHttpRequest, textStatus) {
        var xhrStatus = XMLHttpRequest.status;
        if (xhrStatus == 200 || xhrStatus == 278) {
          if (xhrStatus == 200) {                                 // Form was invalid
            console.log('Form was invalid');

            var form = $(XMLHttpRequest.responseText);
            var modal_body = $(basket_form.parent());
            modal_body.html('');
            modal_body.html(form);

            // remove default cork field
            var default_field = $(data_target).find('#id_corks');
            if (default_field.length > 1) {
              default_field = default_field[0];
              default_field = $(default_field).parents().eq(1);
              $(default_field).remove();
            }

            var row = $(data_target).find('.modal-header div').attr('row');
            var cork = $(data_target).find('.modal-header div').text();

            $(data_target).find('#id_corks option:first').val(row);
            $(data_target).find('#id_corks option:first').text(cork);

            reloadBasketModal('#createBasketCorkModal');    // reload delete reference buttons
            basketModal('#createBasketCorkModal');          // reload reference buttons


            submit_btn.button('reset');
            $(data_target).modal("show");
          }
          else if (xhrStatus == 278) {                            // Form was valid and saved
            console.log('Form was valid and was not returned');
            submit_btn.button('reset');
            $(data_target).modal('hide');
            // window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
          }
        }
      },
      error: function(response) {
        console.log("failure");
        // console.log(request.responseText);
        submit_btn.button('reset');
        $(data_target).find('.alert-danger').remove();
        $(data_target).find('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
        <a class="close" data-dismiss="alert">×</a> \
        There was an error responding to server. Please contact admin. \
        </div>');
      }

    });
    return false;
  });
}

function saveCorkToBasket() {
 $('.editBasket').on('click', function() {
    var cork_id = $(this).attr('row');
    var basket_id = $(this).attr('rowB');
    var basket_title = $(this).text();

    $.ajax({
      beforeSend: function() {
        $('#basketStatusModal .modal-title').html("Add to Basket: "+"<em>"+basket_title+"</em>");
        $('#basketStatusModal p').empty();
        $('#basketStatusModal #loader').show();
      },
      url: '/polls/save_to_basket', 
      data: {'cork_id': cork_id, 'basket_id': basket_id},
      type: 'GET',
      success: function(response) {
        response = JSON.parse(response);
        if (response['status'] == "duplicate error") {
          $('#basketStatusModal p').text("Cork was already added to "+basket_title);
        }
        else 
          $('#basketStatusModal p').text("Cork was added to "+basket_title);
      },
      error: function(response, status, error) {
        $('#basketStatusModal p').text(status+": "+error);
      },
      complete: function() {
        $('#basketStatusModal #loader').hide();
      }
    })
  })
}
function saveCorkToOtherBasket() {
 $('.otherBasket').on('click', function() {

    var cork_id = $(this).attr('row');
    var cork_question = $(this).attr('title');
    $('#editBasketModal p').empty();
    $('#editBasketModal #cork_id option').text(cork_question).val(cork_id);

    save = $('#editBasketModal .btn-primary');

    save.click(function(ev) {
      save.button('loading');
      ev.preventDefault();
      basket = $('#editBasketModal #basket_id option:selected');
      basket_id = basket.val();

      $.ajax({
        url: '/polls/save_to_basket',
        data: {'cork_id': cork_id, 'basket_id': basket_id},
        type: 'GET',
        beforeSend: function() {
          $('#editBasketModal p').empty();
          $('#editBasketModal #loader').show();
        },
        success: function(response) {
          // $('body #wrap #body').append("<div class='alert alert-success alert-dismissable'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>You can now login to projectPear!</div>");
          response = JSON.parse(response);
          if (response['status'] == "duplicate error") {
            $('#editBasketModal p').text("Cork already exists in "+basket.text());
          }
          else {
            $('#editBasketModal p').text("Added cork to "+basket.text());
          }
          // location.reload();
        },
        error: function(response, status, error) {
           $('#editBasketModal p').html('<span class="help-block">'+status+" "+error+'</span>');
           // location.reload();
        },
        complete: function() {
          $('#editBasketModal #loader').hide();
          save.button('reset');
        }
      })
      return false;
    })

  }) 
}

function editCorkForm() {

  $('.item .glyphicon-pencil').click(function() {
    var pencil = $(this);
    
    var POST_URL = "/polls/edit_cork/"+$(this).attr('row');
    modal = $('#editCorkModal');

    // Get the pre-filled form
    $.ajax({
      type: 'GET',
      url: "/polls/edit_cork/"+$(this).attr('row'),
      beforeSend: function() {
        // Loader?
      },
      error: function(request, status, error) {
        // Show error
      },
      success: function(msg) {
        $('#editCorkModal .modal-body').html(msg);
        $('#editCorkModal form').get(0).setAttribute('action', POST_URL);
        $('#editCorkModal').modal('show');
        imageUploadForm(true, '#editCorkModal');
        addChoices('#editCorkModal');
      }
    })

    saveorEditCorkForm('#editCorkButton', '#editCorkForm', '#editCorkModal');

    // There is a known bug when an image and a link are both submitted,
    //    the user will get an error, and the buttons get fucked up

  });
}

function deleteCork(){
  $('.item .glyphicon-trash').click(function() {
    this_cork = $(this).parents('.item'); //get 3rd parent

    var cork_id = $(this).attr('row');
    answer = confirm("Are you sure you want to delete this cork?");
    if (answer) {
      var url = "/polls/delete_cork/"+cork_id;
      // del_cork("/polls/delete_cork/"+cork_id);
      var csrftoken = getCookie('csrftoken');
      $.ajax({
        beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
        },
        type: 'POST',
        url: url,
        success: function(msg){
            // location.reload();  
        },
        error: function(msg) {
            // location.reload();
            // check if alert is already there
            $(this_cork).parents().eq(1).prepend('<div class="alert alert-danger alert-dismissable" style=""> \
                  <button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button> \
                  There was an error processing your deletion. \
                </div>');
        },
        complete: function(xhr) {
            if (xhr.status == 278) {
              $(this_cork).remove();  
              // Repack the corks
              var $container = $('#items');

              $container.masonry({
                itemSelector : '.item',
                columnWidth: 100,
              });
              // window.location.href = xhr.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
            }
        }
      });


    }
  })
}