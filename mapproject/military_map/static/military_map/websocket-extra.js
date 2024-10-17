export const initializeWebSocket = (map, markers, missionroom) => {
    const socket = new WebSocket(
        //'wss://' use this in real deployment.
        'ws://' // use this in development server.
        + window.location.host
        + '/ws/mission/join/'
        + missionroom
        + '/'
    );

    socket.addEventListener('open', e => {
        console.log('WebSocket connection opened.');
    });

    socket.addEventListener('message', (e) => {
        const data = JSON.parse(e.data);
        if (data.type === 'location_point') {
            console.log(data.message);
            const mgrsCoordinates = mgrs.forward([data.longtitude, data.latitude]);
            let receivedUserId = data.user_id;

            // If User's markers already exist, 
            // Update the marker's location 
            //by setting new lat lng
            if (markers[receivedUserId]) {
                markers[receivedUserId]
                .setLatLng([data.latitude, data.longtitude]);

                // Update popup content without reopening it
                const popup = markers[receivedUserId].getPopup();
                if (popup) {
                    popup.setContent(
                        `<p>
                        Name : ${data.full_name}
                        <hr>
                        MGRS : ${mgrsCoordinates}
                        </p>`
                    );
                }
            
            // Else if there's no User's marker yet 
            // Create a new marker for the user
            } else {
                // icon details here 
                let userIcon = L.icon({
                    iconUrl : '/static/military_map/profile.png',
                    iconSize : [40,40],
                    popupAnchor : [0, -10],
                }) 
                // pin marker on map
                markers[receivedUserId] = L
                .marker(
                    [data.latitude, data.longtitude],
                    {icon : userIcon},
                )
                .addTo(map);
                markers[receivedUserId]
                .bindPopup(
                    `<p>
                    Name : ${data.full_name}
                    <hr>
                    MGRS : ${mgrsCoordinates}
                    </p>`,
                    {
                        // leaflet popup options https://leafletjs.com/reference.html#popup
                        closeOnClick: false, 
                        autoClose: false, 
                        autoPan : false,
                    })
                    .openPopup();
            }
        } else if (data.type === "user_disconnect") {
            map.removeLayer(markers[data.user_id]);
            delete markers[data.user_id];
        }
    });

    socket.addEventListener('close', e => {
        console.log('Socket closed');
    });

    return socket;
}