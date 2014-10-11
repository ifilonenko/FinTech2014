/*
*   This is the base javascript file for index.html and base_polls.html
*
*/

$(document).ready(function () {
  openCorkModal();    // Shows createCorkForm Modal onClick
  openBasketModal();
  openClassModal();
  saveorEditCorkForm('#submitCorkButton', '#createCorkForm', '#createCorkModal');   // Saves createCorkForm on Submit
  addChoices('#createCorkForm');
})

function openClassModal() {
  // $('createClassButton').on('click', function(ev) {
  //   var data_target = $(this).attr('data-target');
  //   // $(data_target).find('')
  // });

  $('#createClassModal :submit').on('click', function(ev) {
    ev.preventDefault();
    var submit_btn = $(this);
    var class_form = $('#createClassModal form');
    var data_target = '#createClassModal';

    submit_btn.button('loading');
    class_form.ajaxSubmit({
      complete: function(XMLHttpRequest, textStatus) {
        var xhrStatus = XMLHttpRequest.status;
        if (xhrStatus == 200 || xhrStatus == 278) {
          var form = $(XMLHttpRequest.responseText);
          if (xhrStatus == 200) {                                 // Form was invalid
            console.log('Form was invalid');

            var modal_body = $(class_form.parent());
            modal_body.html('');
            modal_body.html(form);
            
            submit_btn.button('reset');
            $(data_target).modal("show");
          }
          else if (xhrStatus == 278) {                            // Form was valid and saved
            console.log('Form was valid and was not returned');
            submit_btn.button('reset');
            $(data_target).modal('hide');
            location.reload();
            // window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
          }
        }
      },
      error: function() {
        console.log("failure");
        // console.log(request.responseText);
        submit_btn.button('reset');
        if ($(data_target).find('.alert-danger').length == 0) {
          $(data_target).find('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> <a class="close" data-dismiss="alert">×</a> \
          There was an error responding to server. Please contact admin. \
          </div>');
        }
      }
    });
    return false;
  });
  
}

function openBasketModal() {

  basketModal('#createBasketModal');  // load buttons to add references to baskets

  $('#createBasketButton').on('click', function(ev) {
    var data_target = $(this).attr('data-target');
    
    // remove default cork field
    var default_field = $(data_target).find('#id_corks')[0];
    default_field = $(default_field).parents().eq(1);
    $(default_field).remove();

    $('#createBasketModal').modal('show');
  });

  $('#createBasketModal :submit').on('click', function(ev) {
    var submit_btn = $(this);
    var basket_form = $('#createBasketModal form');
    var data_target = '#createBasketModal';

    ev.preventDefault();

    submit_btn.button('loading');
    basket_form.ajaxSubmit({
      complete: function(XMLHttpRequest, textStatus) {
        var xhrStatus = XMLHttpRequest.status;
        if (xhrStatus == 200 || xhrStatus == 278) {
          
          if (xhrStatus == 200) {                                 // Form was invalid
            var form = $(XMLHttpRequest.responseText);
            console.log('Form was invalid');

            var modal_body = $(basket_form.parent());
            modal_body.html('');
            modal_body.html(form);

            // remove default cork field
            var default_field = $(data_target).find('#id_corks')[0];
            default_field = $(default_field).parents().eq(1);
            $(default_field).remove();

            reloadBasketModal('#createBasketModal');    // reload delete reference buttons
            basketModal('#createBasketModal');          // reload reference buttons

            submit_btn.button('reset');
            $(data_target).modal("show");
          }
          else if (xhrStatus == 278) {                            // Form was valid and saved
            console.log('Form was valid and was not returned');
            submit_btn.button('reset');
            $(data_target).modal('hide');
            // window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
            // location.reload();
          }
        }
      },
      error: function() {
        console.log("failure");
        // console.log(request.responseText);
        submit_btn.button('reset');
        if ($(data_target).find('.alert-danger').length == 0) {
          $(data_target).find('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
          <a class="close" data-dismiss="alert">×</a> \
          There was an error responding to server. Please contact admin. \
          </div>');
        }
      }

    });
    return false;
  });
}

function reloadBasketModal(div_to_upload) {
  // var div_to_upload = '#createBasketModal';
  $(div_to_upload+' div #id_references').each(function(index) {
    if (index == 0) return;
    $(this).parent().attr('id', 'extra_input');
    $(this).css('float', 'left').css('width', '92%');
    $(this).parent().append('<a href="#" class="btn btn-small glyphicon glyphicon-remove" style="display: inline; float:right"></a>');
    $(this).parent().next().css('width', '92%');

    $(div_to_upload+' #extra_input .glyphicon-remove').click(function() {
        $(this).parents().eq(1).remove();
        $(div_to_upload+' #add_reference').attr("disabled", false);
        $(div_to_upload+' #add_reference').next('span').remove();
    })
  })
}

function basketModal(div_to_upload) {
  // Load reference buttons
  // var div_to_upload = '#createBasketModal';
  var add_ref = $(div_to_upload+' #add_reference');

  $(add_ref).on('click', function() {
    if ($(div_to_upload+' #id_references').size() < 10) {
      $(add_ref).before(' <div id="extra_input"> \
        <div class="form-group"> \
            <textarea type="text" rows="1" cols="40" style="float: left; width: 92%" class="form-control" id="id_references" name="description" placeholder="Reference" ></textarea> \
            <a href="#" class="btn btn-small glyphicon glyphicon-remove" style="display: inline; float:right"></a> \
          </div> \
          <div class="form-group"> \
            <input type="url" class="form-control"  style="width: 92%" id="id_reference_link" name="link" maxlength="200" placeholder="Link to Reference" /> \
          </div>  \
          </div>');

      $(div_to_upload+' #extra_input .glyphicon-remove').click(function() {
        $(this).parents().eq(1).remove();
        $(div_to_upload+' #add_reference').attr("disabled", false);
        $(div_to_upload+' #add_reference').next('span').remove();
      })
    }
    else {
      $(div_to_upload+' #add_reference').attr("disabled", true);
      $(div_to_upload+' #add_reference').after('<span class="help-block">You cannot add more than 10 references</span>');
    }
  })
}

function openCorkModal() {
  $('#createCorkButton').on('click', function(ev) {
      var data_target = $('#createCorkButton').attr('data-target');
      imageUploadForm(true, '#createCorkForm' );    // Creates the Image File/Link Upload form
      $(data_target).modal('show');
  })
}

/**
*   @param Boolean image_upload: should we upload a file (1) or a link (0) ?
**/
function imageUploadForm(image_upload, div_to_upload) {

  image_upload = typeof image_upload !== 'undefined' ? image_upload : true;

  var question = $(div_to_upload+" .form-group label[for$='id_question']").parent();
  var image_form = $(div_to_upload+" .form-group label[for$='id_image']").parent();
  var image_url_form = $(div_to_upload+" .form-group label[for$='id_image_url']").parent();

  $(image_form).show();
  $(image_url_form).hide();

  if ($(div_to_upload+' .btn-group').length == 0 ) {
     $(question).after('<div class="btn-group" data-toggle="buttons"> \
      <label class="btn btn-large btn-primary" id="file"> \
      <input type="radio" name="file"> Insert Image File \
      </label> \
      <label class="btn btn-large btn-primary" id="link"> \
      <input type="radio" name="link"> Insert Image Link \
      </label> \
      </div>');

     if (image_upload) {                    
      $(div_to_upload+' #file').addClass('active');
     }
     else {
      $(image_form).toggle();
      $(image_url_form).toggle();
      $(div_to_upload+' #link').addClass('active');
     }
  } 

  $(div_to_upload+" .btn-group #file").click(function() {
      $(image_form).show();
      $(image_url_form).hide();
  })

  $(div_to_upload+" .btn-group #link").click(function() {
      $(image_form).hide();
      $(image_url_form).show();
  })

}

function addChoices(div_to_upload) {
  $(div_to_upload+ ' #id_choice').each(function(index) {
      if (index >= 2) {
        var parent = $(this).parent();
        var add_chocie = parent.find('#add_choice');
        $(parent).before('<div class="input-group" id="extra_input"> \
              <span class="input-group-addon"> \
                <input type="radio" disabled="true"/> \
              </span> \
              <input type="text" class="form-control" name="choices" style="width: 90%" value="' + $(this).attr('value') + '"/><a href="#" class="btn btn-small glyphicon glyphicon-remove" style="display-inline"></a> \
            </div>');
        $(parent).remove();
      }
  })

  $(div_to_upload+' #extra_input .glyphicon-remove').click(function() {
        $(this).parent().next().remove();
        $(this).parent().remove();
        $(div_to_upload+' #add_choice').attr("disabled", false);
        $(div_to_upload+' #add_choice').next('span').remove();
  })

  $(div_to_upload+' #add_choice').on('click', function() {
    var count = $(div_to_upload+' #extra_input').length + $(div_to_upload+' #id_choice').length;

    if (count == 10) {
      // There are m choices already, user cannot add more
      $(div_to_upload+' #add_choice').attr("disabled", true);
      $(div_to_upload+' #add_choice').after('<span class="help-block">You cannot add more than 10 choices</span>');
    }
    else {
      $(this).before('<div class="input-group" id="extra_input"> \
              <span class="input-group-addon"> \
                <input type="radio" disabled="true"/> \
              </span> \
              <input type="text" class="form-control" name="choices" style="width: 90%"/> <a href="#" class="btn btn-small glyphicon glyphicon-remove" style="display: inline"></a> \
            </div> <br>')
      $(div_to_upload+' #extra_input .glyphicon-remove').click(function() {
        $(this).parent().next().remove();
        $(this).parent().remove();
        $(div_to_upload+' #add_choice').attr("disabled", false);
        $(div_to_upload+' #add_choice').next('span').remove();
      })
    }
  })
}

function saveorEditCorkForm(submitButton, form_id, modal) {
  $(submitButton).on('click',  function(ev) {

    // ev.preventDefault();

    var self = $(this);
    self.button('loading');
    $(form_id+' #add_choice').attr("disabled", true);
    var submitForm = $(form_id);

    if (form_id == '#editCorkForm') {
      var POST_URL = $(form_id).attr('action');
    }

    // Dependency on the jQuery Form Plugin
    submitForm.ajaxSubmit({
      // beforeSubmit: function(a,f,o) {
      //   o.dataType = 'json';
      // },
      complete: function(XMLHttpRequest, textStatus) {
        var xhrStatus = XMLHttpRequest.status;
        if (xhrStatus == 200 || xhrStatus == 278) {
          var form = $(XMLHttpRequest.responseText);
          if ($(form_id+" #link").hasClass('active')) {    // Upload image
            file_upload_flag = false;
          }
          else {                                                  // Upload Link
            file_upload_flag = true;
          }

          if (xhrStatus == 200) {                                 // Form was invalid
            console.log('Form was invalid');

            var modal_body = $(submitForm.parent());
            modal_body.html('');
            modal_body.html(form);
            imageUploadForm(file_upload_flag, form_id );
            addChoices(form_id);

            if (form_id == '#editCorkForm') {
              $('#editCorkModal form').get(0).setAttribute('action', POST_URL);
            }
            
            self.button('reset');
            $(modal).modal("show");
          }
          else if (xhrStatus == 278) {                            // Form was valid and saved
            console.log('Form was valid and was not returned');
            self.button('reset');
            $(modal).modal('hide');
            window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
          }
        }
      },
      error: function(request, status, error) {
          //implement proper error handling
          console.log("failure");
          // console.log(request.responseText);
          self.button('reset');
          $('#add_choice').attr("disabled", false);
          if (submitForm.parents().eq(1).find('.alert-danger').length == 0) {
            submitForm.parents().eq(1).children('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
            <a class="close" data-dismiss="alert">×</a> \
            There was an error responding to server. Please contact admin. \
            </div>');
          }
          

        }
    });

    // !!! Important !!! 
    // always return false to prevent standard browser submit and page navigation
    return false;
  })
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}