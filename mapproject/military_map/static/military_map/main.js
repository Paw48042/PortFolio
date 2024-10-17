import { initializeMap } from './map.js';
import { initializeWebSocket } from './websocket-extra.js';
import { watchUserPosition } from './geolocation.js';
import { getUserId, getMissionRoom, getMissionOwner, getFullName } from './dom.js';

document.addEventListener('DOMContentLoaded', () => {
    const { map, markers, drawnItems } = initializeMap();
    const userId = getUserId();
    const fullName = getFullName();
    const missionroom = getMissionRoom();
    const missionOwner = getMissionOwner();
    const socket = initializeWebSocket(map, markers, missionroom);
    watchUserPosition(socket, userId, fullName);

    // get the drawing
    // Fetch and add existing drawings to the map
    fetch(`/get_drawings/${missionroom}`)
        .then(response => response.json())
        .then(data => {
            L.geoJSON(data, {
                onEachFeature: (feature, layer) => {
                    if (feature.properties && feature.properties.name) {
                        layer.bindPopup(feature.properties.name,
                            {
                                closeOnClick: false, 
                                autoClose: false,
                                autoPan : false,
                            }).openPopup();
                        
                        if(feature.geometry.type !== 'Point'){

                            layer.setStyle({
                                color: feature.properties.color,
                                fillColor: feature.properties.fillColor
                            })
                        }
                    }
                    // Ensure only editable layers are added
                    if (layer instanceof L.Polygon || layer instanceof L.Polyline || layer instanceof L.Marker) {
                        drawnItems.addLayer(layer);
                    }
                }
            }).addTo(map);
        });
});