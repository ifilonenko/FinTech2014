/*
* Function to edit a basket
*/

$(document).ready(function () {

    edit_basket_title_reference();      // function to edit title/reference in basket
    basketModal('#editBasketStuffModal');

    basket_edit_dict = {
        "deleted": [],
        "sorting": [],
    }
    var pckry;
    var basket_id = $('#items').attr('row');

    $('.edit').click(function() {
        if (!$(this).hasClass('active')) {
            $(this).toggleClass('active');
            $('#userEditOptions').toggleClass('hidden');
            $('.item #corkEditNav').each(function() {
                $(this).toggleClass('hidden');    
            })
            $(this).text("Editing...");    

            var $container = $('.packery-container');
            $container.packery({
                columnWidth: 300,
                rowHeight: 150,
                gutter: 5
            });
            // get item elements, jQuery-ify them
            var $itemElems = $( $container.packery('getItemElements') );

            // make item elements draggable
            $itemElems.draggable();

            // bind Draggable events to Packery
            $container.packery( 'bindUIDraggableEvents', $itemElems );

            pckry = $container.data('packery');


            $('#corkEditNav .glyphicon-remove').click( function() {
                item = $(this).parent().parent();
                
                if ($(this).hasClass("glyphicon-ok")) {
                    item.css({opacity: 1});
                }
                else {
                    item.css({opacity: 0.5});
                    // Append deleted item
                    // $container.packery('addItems', item);
                    // $container.packery().append(item);
                }
                $(this).toggleClass("glyphicon-ok");
                $(this).toggleClass("glyphicon-remove");
                $container.packery();
            })

        }//end if Edit active
        else {}
    })

   $('#userEditOptions .glyphicon-trash').click(function() {
        if ($('.edit').hasClass('active')) {
             answer = confirm("Are you sure you want to delete this basket?");
            if (answer) {
                resetButtons(this);
                edit_basket("/polls/delete_basket/"+basket_id);
            }

        }
    })//end delete basket

    $('#userEditOptions .glyphicon-floppy-save').click(function() {
        if ($('.edit').hasClass('active')) {
            
            orderedItems = pckry.getItemElements();
            basket_edit_dict.sorting = [];
            basket_edit_dict.deleted = [];

            for (var i = 0 ; i < orderedItems.length; i++) {
                if ($(orderedItems[i]).css('opacity') == 1 && $(orderedItems[i]).hasClass('item'))
                    basket_edit_dict.sorting.push({ 
                        'cork_id': $(orderedItems[i]).attr('row'),
                        'position': i
                        });
                else
                    basket_edit_dict.deleted.push( $(orderedItems[i]).attr('row') );
            }

            resetButtons(this);
            // if (basket_edit_dict.sorting[0] != undefined || basket_edit_dict.deleted[0] != undefined )
            edit_basket("/polls/edit_basket_save/"+basket_id, JSON.stringify(basket_edit_dict));
        }
    })

    $('#userEditOptions #cancel').click(function() {
        if ($('.edit').hasClass('active')) {
            resetButtons(this);
            var $itemElems = $( $container.packery('getItemElements') );

            // make item elements draggable
            $itemElems.draggable('destroy');
            $container.packery('destroy');
        }
    })

})

function resetButtons(obj) {
    $('.edit').toggleClass('active');
    $('#userEditOptions').toggleClass('hidden');
    $('.item #corkEditNav').each(function() {
      $(this).toggleClass('hidden');    
    })
    $('.edit').text("Edit Corks"); 

    // $container.packery('destroy');
}

function removeByValue(arr, val) {
    for(var i=0; i<arr.length; i++) {
        if(arr[i] == val) {
            arr.splice(i, 1);
            break;
        }
    }
}

function edit_basket(url, data) {
    var csrftoken = getCookie('csrftoken');

    $.ajax({

        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        
        type: 'POST',

        url: url,
        data: {json_data: data},

        success: function(msg){
            // location.reload();             
        },
        error: function(msg) {
            // location.reload();
        },
        complete: function(xhr) {
            if (xhr.status == 278) {
                window.location.href = xhr.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
            }
            else {
                location.reload();
            }
        }
    });
}

function edit_basket_title_reference() {
    
    var edit_btn = '.edit_basket';

    var POST_URL = "/polls/edit_basket/"+$(edit_btn).attr('row');
    modal = '#editBasketStuffModal';

    // Get the pre-filled form
    $.ajax({
        type: 'GET',
        url: POST_URL,
        beforeSend: function() {
        // Loader?
        },
        error: function(request, status, error) {
        // Show error
        },
        success: function(msg) {
            $(modal+' .modal-body').html(msg);
            $(modal+' form').get(0).setAttribute('action', POST_URL);
            $(modal+' label').each(function() {
                if ($(this).attr('for') == "id_corks") {
                   $(this).next().remove(); 
                   $(this).remove();
                }  
            })
            reloadBasketModal(modal);
            basketModal(modal);
        }
    })

    $(modal+' button:submit').click(function(ev) {
        ev.preventDefault();

        var btn = $(this);
        btn.button('loading');
        $(modal+' add_reference').attr('disabled', true);

        var form = $(modal).find('form');
        form.ajaxSubmit({
            complete: function(xhr, textStatus) {
                var xhrStatus = xhr.status;
                if (xhrStatus == 200 || xhrStatus == 278) {
                    var new_form = $(xhr.responseText);

                    if (xhrStatus == 200) {     // Form invalid
                        console.log("Form was invalid");
                        var modal_body = $(form.parent());
                        modal_body.html('');
                        modal_body.html(new_form);
                        $(modal+' form').get(0).setAttribute('action', POST_URL);
                        $(modal+' label').each(function() {
                            if ($(this).attr('for') == "id_corks") {
                               $(this).next().remove(); 
                               $(this).remove();
                            }  
                        })
                        $(modal).modal('show');
                        btn.button('reset');
                    }
                    else if (xhrStatus == 278) {
                        btn.button('reset');
                        $(modal).modal('hide');
                        // window.location.href = xhr.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
                        location.reload();
                    }
                }
            },
            error: function(request, status, error) {
                console.log("failure");
              // console.log(request.responseText);
              btn.button('reset');
              if (form.parents().eq(1).find('.alert-danger').length == 0) {
                form.parents().eq(1).children('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
                <a class="close" data-dismiss="alert">×</a> \
                There was an error responding to server. Please contact admin. \
                </div>');
              }
            }
        });
        return false;
    });
}

function update_edit_modal(modal) {
    var add_ref = modal+' #add_reference';
            $(add_ref).click(function() {
                if ($(modal+' #id_references').size() < 10) {
                    $(add_ref).before(' <div id="extra_input"> \
                    <div class="form-group"> \
                    <textarea type="text" rows="1" cols="40" style="float: left; width: 92%" class="form-control" id="id_references" name="description" placeholder="Reference" ></textarea> \
                    <a href="#" class="btn btn-small glyphicon glyphicon-remove" style="display: inline; float:right"></a> \
                    </div> \
                    <div class="form-group"> \
                    <input type="url" class="form-control"  style="width: 92%" id="id_reference_link" name="link" maxlength="200" placeholder="Link to Reference" /> \
                    </div>  \
                    </div>');

                    $(modal+' #extra_input .glyphicon-remove').click(function() {
                    $(this).parents().eq(1).remove();
                    $(modal+' #add_reference').attr("disabled", false);
                    $(modal+' #add_reference').next('span').remove();
                    })
                }
                else {
                    $(modal+' #add_reference').attr("disabled", true);
                    $(modal+' #add_reference').after('<span class="help-block">You cannot add more than 10 references</span>');
                }
            })
}

