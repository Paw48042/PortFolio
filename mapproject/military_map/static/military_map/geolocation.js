export const watchUserPosition = (socket, userId, fullName) => {
    if ('geolocation' in navigator) {
        navigator.geolocation.watchPosition(
            //success
            (position) => {
                let lat = position.coords.latitude;
                let lon = position.coords.longitude;
                let acc = position.coords.accuracy;
                const message = `Position is LAT: ${lat}, LON: ${lon} and has an accuracy of ${acc} meters.`;
                socket.send(JSON.stringify({
                    'message': message,
                    'latitude': lat,
                    'longtitude': lon,
                    'accuracy': acc,
                    'user_id': userId,
                    'full_name' : fullName
                }));
            },
            //error
            (error) => {
                console.log('The Error has occurred.');
                console.log(error);
            },
            // options
            {
                maximumAge : 0,
                enableHighAccuracy : true,
                
            }
        );
    } else {
        console.log('Geo Location is not supported by this browser.');
    }
}