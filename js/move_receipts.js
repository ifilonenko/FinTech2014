

$(document).ready(function () {

    console.log("aslkdjfalksjdf");
    var pckry;

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

    console.log("asdf");



})

