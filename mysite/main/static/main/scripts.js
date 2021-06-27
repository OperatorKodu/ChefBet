window.addEventListener('DOMContentLoaded', event => {

    // Toggle the side navigation
    const sidebarToggle = document.body.querySelector('#sidebarToggle');
    if (sidebarToggle) {
        // Uncomment Below to persist sidebar toggle between refreshes
        // if (localStorage.getItem('sb|sidebar-toggle') === 'true') {
        //     document.body.classList.toggle('sb-sidenav-toggled');
        // }
        sidebarToggle.addEventListener('click', event => {
            event.preventDefault();
            document.body.classList.toggle('sb-sidenav-toggled');
            localStorage.setItem('sb|sidebar-toggle', document.body.classList.contains('sb-sidenav-toggled'));
        });
    }

    $(document).on('click', '.odds-btn', function(e){
        var source = $(e.target);
        var classes = source.attr('class').split(' ');
        var event_id = classes[0];
        var type = classes[1];
        var type_description = classes[2];
        var event;

        $.ajax({
            url: "/events/",
            type: "GET",
            dataType: "json",
        }).done(function( json ) {
            json.forEach(function(obj) {
                if (parseInt(obj.id) === parseInt(event_id)) {
                    event = obj;
                    $('#coupon-events-table').find('tbody').append("<tr id='" + event_id + "'><td id='event_name'>" + event.host + " vs " + event.guest + "</td><td id='type_desc'>"+ type_description + ": " + type +"</td><td id='odds'>" + event.types[type_description][type] + "</td></tr>");
                }
            });
        }).fail(function( xhr, status, errorThrown ) {
            alert("Nie udalo sie pobrac danych.");
        });
        var summary_odds = 1;
        $('#coupon-events-table tbody tr').each(function (){
            summary_odds = summary_odds * parseFloat($(this).find('#odds').text());
            console.log($(this).find('#odds').text());
        });
        $('#summary-odds').text(summary_odds);
        var summary_prize = parseFloat($('#summary-contribution').val()) * summary_odds;
        $('#summary-prize').text(summary_prize);
    });

});
