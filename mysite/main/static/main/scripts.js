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

        function tableContains(id){
            let matched = false;
            $('#coupon-events-table tbody tr').each(function (){
                //console.log($(this).attr('id') + "=" + parseInt(id));
                if (parseInt($(this).attr('id')) === parseInt(id)){
                    matched = true
                    return true;
                }
            });
            return matched;
        }

        var source = $(e.target);
        var classes = source.attr('class').split(' ');
        var event_id = classes[0];
        var type = classes[1];
        if (classes[2] === "Wynik") {
            var type_description = "Wynik";
        } else {
            var type_description = source.parent().parent().parent().parent().parent().parent().find('.more-event-description').text();
            //var type_description = "Wynik";
            console.log(type_description);
        }
        var event_name;
        var odds;

        if (tableContains(event_id)){
            alert('Zakład dotyczący tego wydarzenia już istnieje');
        }else {

            $.ajax({
                url: "/events/",
                type: "GET",
                dataType: "json",
            }).done(function (json) {
                json.forEach(function (obj) {
                    if (parseInt(obj.id) === parseInt(event_id)) {
                        let event = obj;
                        event_name = event.host + " vs " + event.guest;
                        odds = parseFloat(event.types[type_description][type]);
                        $('#coupon-events-table').find('tbody').append("<tr id='" + event_id + "'><td id='event_name'>" + event_name + "</td><td id='type_desc'>" + type_description + ": " + type + "</td><td id='odds'>" + odds + "</td></tr>");
                        let old_odds = parseFloat($('#summary-odds').text());
                        let summary_odds = old_odds * odds;
                        console.log(summary_odds);
                        $('#summary-odds').text(summary_odds);
                        let summary_prize = parseFloat($('#summary-contribution').val()) * summary_odds;
                        $('#summary-prize').text(summary_prize);
                    }
                });
            }).fail(function (xhr, status, errorThrown) {
                alert("Nie udalo sie pobrac danych.");
            });
        }

        $('#clear-coupon-btn').click(function () {
            $('#coupon-events-table tbody').empty();
            $('#summary-odds').text(1);
            $('#summary-contribution').val(5);
            $('#summary-prize').text(0);
        });

        $('#submit-coupon-btn').click(function () {

        });
    });

});
