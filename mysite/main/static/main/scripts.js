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

    function displayWalletContent() {
        $.ajax({
            url: "/wallets/",
            type: "GET",
            dataType: "json",
        }).done(function (json) {
            json.forEach(function (wallet) {
                $('#wallet-content').val(wallet.money);
            });
        });
    }

    function topUpWalletContent(money) {
        const csrftoken = getCookie('csrftoken');
        let data = {"money": money};
        $.ajax({
            type: 'PUT',
            url: '/wallets/1/',
            headers: {"X-CSRFToken": csrftoken},
            contentType: 'application/json',
            data: JSON.stringify(data), // access in body
        }).done(function () {
            console.log('SUCCESS');
        }).fail(function (msg) {
            console.log('FAIL');
        });
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
    displayWalletContent();
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

        let source = $(e.target);
        let classes = source.attr('class').split(' ');
        let event_id = classes[0];
        let type_id = parseInt(classes[1]);
        let type = classes[2];

        if (tableContains(event_id)) {
            alert('Zakład dotyczący tego wydarzenia już istnieje');
        } else {

            $.ajax({
                url: "/events/" + event_id + "/",
                type: "GET",
                dataType: "json",
            }).done(function (event) {
                let possibilities = event.types[type_id-1].possibilities;
                let event_name = event.host + " vs " + event.guest;
                let odds;
                for (let i = 0; i < possibilities.length; i++) {
                    if (possibilities[i][type] != null) {
                        odds = possibilities[i][type];
                        break;
                    }
                }

                $('#coupon-events-table').find('tbody').append(
                    "<tr id='" + event_id + "' class='" + type_id + "'>" +
                        "<td id='event_name'>" + event_name + "</td>" +
                        "<td id='type_desc'>" + event.types[type_id-1].description + ": " + type + "</td>" +
                        "<td id='odds'>" + odds + "</td>" +
                    "</tr>"
                );

                let old_odds = parseFloat($('#summary-odds').text());
                        let summary_odds = old_odds * odds;
                        console.log(summary_odds);
                        $('#summary-odds').text(summary_odds);
                        let summary_prize = parseFloat($('#summary-contribution').val()) * summary_odds;
                        $('#summary-prize').text(summary_prize);

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
        if (document.getElementById('user_id') == null) {
            alert('Tylko zalogowani użytkownicy mogą obstawiać');
        } else {
            const user_id = JSON.parse(document.getElementById('user_id').textContent);
            const csrftoken = getCookie('csrftoken');
            let types = '{"types": [';
            $('#coupon-events-table tbody').find('tr').each(function () {
                let event_id = $(this).attr('id');
                let type_id = $(this).attr('class');
                let type_desc = $(this).find('#type_desc').text();
                let type = type_desc.split(':')[1].trimLeft();
                types = types + '{"event_id": ' + event_id + ', "type_id": ' + type_id + ', "type": "' + type + '"},';
            })
            types = types.slice(0, -1) + '],';
            let contribution = '"contribution": ' + $('#summary-contribution').val() + '}';

            let coupon = JSON.parse(types + contribution);

            let newMoney = parseFloat($("#wallet-content").val()) - parseFloat($('#summary-contribution').val());
            if (newMoney >= 0) {
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
                    topUpWalletContent(newMoney);
                    displayWalletContent();
                },
                error: function (errMsg) {
                    alert("Cosik posło nie tak");
                }
            });
            } else {
                alert("Brak środków w portfelu");
            }
        }
    });

    $('#top-up-wallet').click(function () {
        topUpWalletContent(parseFloat($('#top-up-amount').val()));
        displayWalletContent();
    });

});
