/**
*
*   User Profile js functions
**/

function get_tab(url, page) {

    var element = $('#pane_container').children("#items");
    var loader = $('#pane_container').children("#loader");

    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            element.hide();
            loader.show();
        },
        type: 'POST',
        data: {
            'page': page,
        //    'class_id': class_id
        },
        url: url,
        complete: function() {
            loader.hide();
            element.show();
        },
        success: function(msg){
            element.html(msg);

            submenu();
            addCorkToBasketModal();
            saveCorkToBasket();
            saveCorkToOtherBasket();
            editCorkForm();
            deleteCork();
        },
        error: function(msg) {
            element.html(msg);
        }
    });
}


function manage_relationship(url) {
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
    		location.reload();
    	},
    	error: function(msg) {
    		location.reload();
    	}
});
}