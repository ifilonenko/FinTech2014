/**
*      
**/
function get_tab(url, class_id, page, student_id) {

	var element = $('#class_baskets').children("#tab_content");
    var loader = $('#class_baskets').children("#loader");

    data = {
        'page': page,
        'class_id': class_id
    }
    if (student_id != undefined) {
        if (confirm("Are you sure you want to remove this student from your class?!"))
            data['student_id'] = student_id;
        else    return;
    }

	$.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            
            if (url != "/classes/ajax/cork_viewing") {// no loader in cork_viewer
                element.hide();
                loader.show();
            }
        },
        type: 'POST',
        data: data,
        url: url,
        complete: function() {
            loader.hide();
            element.show();
        },
        success: function(msg){
            element.html(msg);
            if (url == "/classes/ajax/get/baskets") {
                edit_basket_order(class_id, element);
            }
            else if (url == "/classes/ajax/manage_voting") {
                open_manage_voting_tab();
            }
        },
        error: function(msg) {
            element.html(msg);
        }
    });
}

function manage_enrollment(url, class_id, action) {

	$.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            $('#enroll_button').hide();
        },
        type: 'POST',
        data: {
        	'action': action,
        	'class_id': class_id
        },
        url: url,
        success: function(msg){
            if (msg.result == "failed") {
                $('#tab_content').append("<p>"+msg.reason+"</p>");
            }
            else 
                location.reload();
        },
        error: function(msg) {
            location.reload();
        }
    });
}

function edit_class(url, form) {
    var form = $(form);
    var tabContent = form.parent();
    var submit_btn = form.find('a.btn-primary');
    submit_btn.button('loading');

    form.ajaxSubmit({
        complete: function(XMLHttpRequest, textStatus) {
            
            var xhrStatus = XMLHttpRequest.status;

            if (xhrStatus == 278) {          // Form valid
                // window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
                location.reload();
            }
            else if (xhrStatus == 200) {    // Form invalid
                // Form was invalid
                submit_btn.button('reset');
                tabContent.empty();
                tabContent.append(XMLHttpRequest.responseText);
            }            
        },
        error: function(response) {
            console.log(response);
            // console.log(request.responseText);
            submit_btn.button('reset');
            tabContent.find('.alert-danger').remove();
            tabContent.first('p').prepend('<div style="text-align: center;" class="alert alert-danger"> \
                <a class="close" data-dismiss="alert">×</a> \
                There was an error responding to server. Please contact admin. \
                </div>');
        }
    });

}
function delete_class(url) {
    if (confirm("Are you sure you want to delete this class forever?!")) {
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
                $('#deleteButton').button('loading');
            },
            type: 'POST',
            url: url,
            complete: function(XMLHttpRequest, textStatus) {
                console.log(XMLHttpRequest);
                var xhrStatus = XMLHttpRequest.status;
                if (xhrStatus == 278) {
                    window.location.href = XMLHttpRequest.getResponseHeader("Location").replace(/\?.*$/, "?next="+window.location.pathname);
                }
            },
            success: function(msg){
                // location.reload();
            },
            error: function(msg) {
                // handle error?
                location.reload();
            }
        });
    }
}

function edit_basket_order(class_id, element) {
    var cancel = $('.glyphicon-minus');
    var update = $('.glyphicon-floppy-save');

    // get last basket_id that was open for voting
    var last_basket_vote = false;
    $('#sortable_baskets li').each(function() {
        if ($(this).find('#vote').hasClass('glyphicon-pencil')) {
            last_basket_vote = $(this).attr('row');
            return false;
        }
    });

    cancel.on('click', function() {
        $('#classEdit').button('reset');
        $('#classEdit').toggleClass('active');
        $('#classEditOptions').toggleClass('hidden');
        $('.row #items').toggleClass('hidden');
        update.button('reset');
    }); 

    update.on('click', function() {
        // AJAX!
        $(this).button('loading');
        cancel.button('loading');
        var url = "/classes/ajax/basket_order_votes";

        var class_edit_dict = {
            "deleted": [],
            "sorting": [],
        }
        class_edit_dict.sorting = [];
        class_edit_dict.deleted = [];

        var this_basket_vote = false;

        var count = 0;
        $('#sortable_baskets li').each(function() {
            row = $(this).attr('row');
            if ($(this).find('#delete').hasClass('glyphicon-ok'))
                class_edit_dict.deleted.push(row);
            else {
                class_edit_dict.sorting.push({
                    'basket_id': row,
                    'position': count
                }); 
                count++;
            }

            if ($(this).find('#vote').hasClass('glyphicon-pencil'))
                this_basket_vote = row;
        })

        // Open basket for voting
        var data = {};
        if (last_basket_vote != this_basket_vote) {
            if (this_basket_vote != false)
                data['basket_class_id'] = this_basket_vote;

            if (last_basket_vote != false)
                data['last_basket_class_id'] = last_basket_vote
        }

        data['class_id'] = class_id;
        data['json_data'] = JSON.stringify(class_edit_dict);
        $.ajax({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            type: 'POST',
            data: data,
            url: url,
            success: function(msg){
                element.html(msg);

                edit_basket_order(class_id, element);
                
            },
            error: function(msg) {
                console.log(msg);
            }
        })
    });
}

function toggle_info(id) {
    // $(id).toggleClass("hidden");
    if ($(id).css("display") == "none") {
        $(id).fadeIn("fast");
    }
    else
        $(id).fadeOut("fast");
}

function delete_basket(basket_id) {

    var elem = $('#sortable_baskets li[row='+basket_id.toString()+']');

    if (elem.find('#delete').hasClass('glyphicon-remove'))
        elem.fadeTo("fast", 0.5);
    else
        elem.fadeTo("fast", 1);
    
    var btn = elem.find('#delete');
    $(btn).toggleClass('glyphicon-remove');
    $(btn).toggleClass('glyphicon-ok');
}

function open_basket_voting(basket_id) {
    $('#sortable_baskets li').each(function() {        // disable buttons before processing
        $(this).find('#vote').attr('disabled', 'disabled');
    })

    var elem = $('#sortable_baskets li[row='+basket_id.toString()+']');
    var btn = elem.find('#vote');
    var nextBtn;
    var voting = false;

    if ($(btn).hasClass('btn-success')) {
        toggle_vote(btn);
        $('#sortable_baskets li').each(function() {        // enable buttons
            $(this).find('#vote').removeAttr('disabled');
        })
        return false;
    }

    $('#sortable_baskets li').each(function() {
        nextBtn = $(this).find('#vote');
        if (btn != $(nextBtn) && $(nextBtn).hasClass('btn-success')) {
            toggle_vote(btn);
            toggle_vote(nextBtn);
            voting = true;
            return false;
        }
    })   

    if (!voting) toggle_vote(btn);

    $('#sortable_baskets li').each(function() {        // enable buttons
        $(this).find('#vote').removeAttr('disabled');
    })


}

function toggle_vote(btn) {
    $(btn).toggleClass('glyphicon-bell');
    $(btn).toggleClass('glyphicon-pencil');
    $(btn).toggleClass('btn-info');
    $(btn).toggleClass('btn-success');
}

function edit_baskets_in_class(btn) {
    btn = $(btn);

    if (!btn.hasClass('active')) {
        // console.log('is active');
        btn.toggleClass('active');
        btn.button('loading');

        $('#classEditOptions').toggleClass('hidden');
        $('.row #items').toggleClass('hidden');
        $('#sortable_baskets').sortable();
    }
}


