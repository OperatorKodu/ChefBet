window.addEventListener('DOMContentLoaded', event => {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

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

    $(document).on('click', '.odds-btn', function (e) {

        function tableContains(id) {
            let matched = false;
            $('#coupon-events-table tbody tr').each(function () {
                //console.log($(this).attr('id') + "=" + parseInt(id));
                if (parseInt($(this).attr('id')) === parseInt(id)) {
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

        if (tableContains(event_id)) {
            alert('Zakład dotyczący tego wydarzenia już istnieje');
        } else {

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
    });

    $('#clear-coupon-btn').click(function () {
        $('#coupon-events-table tbody').empty();
        $('#summary-odds').text(1);
        $('#summary-contribution').val(5);
        $('#summary-prize').text(0);
    });

    $('#submit-coupon-btn').click(function () {

        const csrftoken = getCookie('csrftoken');
        let types = '{"types": [';
        $('#coupon-events-table tbody').find('tr').each(function () {
            let event_id = $(this).attr('id');
            let text = $(this).find('#type_desc').text();
            text = text.split(':');
            types = types + '{"event_id": ' + event_id + ', "' + text[0] + '": "' + text[1].trimLeft() + '"},';
        })
        types = types.slice(0, -1) + '],';
        let odds = '"odds": ' + $('#summary-odds').text() + ',';
        let contribution = '"contribution": ' + $('#summary-contribution').val() + ',';
        let prize = '"prize": ' + $('#summary-prize').text() + ',';
        const user_id = JSON.parse(document.getElementById('user_id').textContent);
        let author = '"author": "http://127.0.0.1:8000/users/' + user_id + '/"}';

        let coupon = JSON.parse(types + odds + contribution + prize + author);

        $.ajax({
            type: "POST",
            url: "/coupons/",
            // The key needs to match your method's input parameter (case-sensitive).
            data: JSON.stringify(coupon),
            headers: {"X-CSRFToken": csrftoken},
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                alert("Pomyślnie postawiono kuponik");
            },
            error: function (errMsg) {
                alert("Cosik posło nie tak");
            }
        });
    });

});
