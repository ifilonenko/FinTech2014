
function load_stats_tab() {
    // Find the current basket open_for_voting and load the votes for that basket
    $('#accordion').on('show.bs.collapse', function(ev) {

      if ($(ev.target).hasClass('outer_accordion')) {

        var element_id = $(ev.target).attr("id");
        var element = $('#'+element_id) ;
        var basket_id = $(ev.target).attr("basket");
        var class_id = $(ev.target).attr("tclass");
        var url = $(ev.target).attr("URL");

        data['class_id'] = class_id;
        data['basket_id'] = basket_id;

        $.ajax({
          beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
            element.children().html(''); 
            element.parent().find('#loader').show();
        },
        type: 'POST',
        data: data,
        url: url,
        complete: function() {
            element.parent().find('#loader').hide();
            plot_bar_graphs();
        },
        success: function(msg){
            // console.log(msg);
            element.children().html(msg);
        },
        error: function(msg) {
            element.children().html('<span class="help-block">There was an error responding to server. Contact admin.</span>');
        }
        });
      }

    })
}

function plot_bar_graphs() {
    $('.panel-body').find('table').each(function() {
        $(this).highchartTable();
    });
}



