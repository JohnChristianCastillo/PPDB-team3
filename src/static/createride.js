// make a map that will be placed on the 'Create a ride' page
let map2 = L.map('createride_map').setView([51, 4.4], 10);

// add a tile layer to the (empty) map
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map2);

map2.on('click', function (e) {
    var container = L.DomUtil.create('div'),
        startBtn = createButton('Start from this location', container),
        destBtn = createButton('Go to this location', container);

    L.popup()
        .setContent(container)
        .setLatLng(e.latlng)
        .openOn(map2);
    L.DomEvent.on(startBtn, 'click', function () {
        control.spliceWaypoints(0, 1, e.latlng);
        map2.closePopup();
    });

    L.DomEvent.on(destBtn, 'click', function () {
        control.spliceWaypoints(control.getWaypoints().length - 1, 1, e.latlng);
        map2.closePopup();
    });
});

L.Routing.control({
    serviceUrl: 'http://127.0.0.1:5001/route/v1',
    routeWhileDragging: true,
    geocoder: L.Control.Geocoder.nominatim()
})
    // when route is found, send coordinates of start and end to /en/receiver
    .on('routesfound', function (e) {
        let from = e.waypoints[0].latLng;
        let to = e.waypoints[1].latLng;
        $.post({
            contentType: "application/json",
            url: "/en/receiver",
            data: JSON.stringify({from: from, to: to})
        })
            // when post request is done, get the returned data and do something with it
            .done(function (data) { // response function
                alert("Result: " + data);
            });
    }).addTo(map2);
