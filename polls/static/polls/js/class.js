/*
* Function to add a basket to class
*/

$(document).ready(function(){
    $('#basketClassModal').on('hidden.bs.modal', function() {
        $(this).find(':submit').unbind();   //Unbind click event when modal is closed
        $(this).find('p').empty();
    })
})

// Add a basket to a class
function addBasketToClass(url, data_target, basket_name, basket_id) {

    $(data_target).find('#basket_id option:first').val(basket_id).text(decodeURI(basket_name));
    $(data_target).modal('show');

    $('#basketClassModal :submit').on('click', function(ev) {
        ev.preventDefault();
        var submit_btn = $(this);
        submit_btn.button('loading');
        var class_id = $(data_target).find('#class_id option:selected');

        $(data_target).find('#loader').show();

        $.ajax({
            beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
              }
            },
            url: '/classes/ajax/add_basket_to_class',
            data: {'class_id': class_id.val(), 'basket_id': basket_id},
            type: 'POST',
            success: function(response) {
                response = JSON.parse(response);
                if (response.status == "ok") {
                     $(data_target).find('p').text("Basket was added succesfully");
                }
            },
            error: function(response, status, error) {
                if (response.status == 404) {
                    $(data_target).find('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
                        <a class="close" data-dismiss="alert">×</a> \
                        You must add a class form the navbar! \
                        </div>');
                }
                else if (response.status == 400 && JSON.parse(response.responseText).status == "duplicate error") {
                    $(data_target).find('p').text("Basket already exists in this class");
                }
                else {
                    $(data_target).find('.alert-danger').remove();
                    $(data_target).find('.modal-footer').prepend('<div style="text-align: center;" class="alert alert-danger"> \
                        <a class="close" data-dismiss="alert">×</a> \
                        There was an error responding to server. Please contact admin. \
                        </div>');
                }
            },
            complete: function() {
                $(data_target).find('#loader').hide();
                submit_btn.button('reset');
            }
        });
        return false;
    });
}