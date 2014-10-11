
function open_manage_voting_tab() {

    $('#selectable_corks a').on('click', function() {
        var selection = $(this);

        $('#selectable_corks a').each(function() {
            if ($(this).hasClass('active')) {
                $(this).toggleClass('active');
            }

            if (selection.attr('row') == $(this).attr('row') && $(this).find('#first_second_vote').length == 0) {
                $(this).append('<span style="float: right" id="first_second_vote">First vote</span>');
            }
            else if (selection.attr('row') == $(this).attr('row') && $(this).find('#first_second_vote').text() == "First vote") {
                $(this).find('#first_second_vote').text('Second vote');
            }
            else if (selection.attr('row') == $(this).attr('row') && $(this).find('#first_second_vote').text() == "Second vote") {
                $(this).find('#first_second_vote').remove();
                $(this).toggleClass('active');
            }
            else if (selection.attr('row') != $(this).attr('row'))
                $(this).find('#first_second_vote').remove();

        });
        $(this).toggleClass('active');
    });
}

function makeEmVote(basket_class_id, btn, url) {

    // test this for an empty basket...

    var second_vote;         // True = second vote, False = first vote
    var cork_to_vote_on;

    $('#selectable_corks a').each(function() {
        if ($(this).hasClass('active')) {
            cork_to_vote_on = $(this).attr('row');

            if ($(this).find('#first_second_vote').text() == "First vote")
                second_vote = '';       //false
            else
                second_vote = true;

            return false;
        }
    });

    if (second_vote == undefined || cork_to_vote_on == undefined) {
        data = {
            'basket_class_id': basket_class_id,
            'reset_votes': true
        }
    }
    else 
        data = {
            'basket_class_id': basket_class_id,
            'second_vote': second_vote,
            'cork_to_vote_on': cork_to_vote_on
        }

    $.ajax({
         beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            $(btn).button('loading');
        },
        type: 'POST',
        data: data,
        url: url,
        complete: function() {
            $(btn).button('reset');
        },
        success: function(msg){
            // console.log(msg);
            if ( !$(btn).next().hasClass('alert') ) {
                $(btn).after('<div class="alert alert-info" style="text-align: center;"> \
                        Saved Successfully! \
                      </div>');
                $(btn).next().fadeOut(1700, function() {
                    $(this).remove();
                });
            }
            return false;
        },
        error: function(msg) {
            // console.log(msg);
            if ( !$(btn).next().hasClass('alert') ) {
                $(btn).after('<div class="alert alert-danger" style="text-align: center;"> <a class="close" data-dismiss="alert">×</a> \
                      There was an error, contact admin. \
                      </div>');
            }
            return false;
        }
    });

}