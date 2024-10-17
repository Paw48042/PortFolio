import { getMissionRoom, getMissionOwner, getUserId } from "./dom.js";

export const initializeMap = () => {
    let markers = {};
    var map = L.map('map').setView([14.088987636381693, 99.429766366867], 12);
    const missionroom = getMissionRoom();
    const missionOwner = getMissionOwner();
    const userId = getUserId();

    // modal element 
    // shape name to input shape name 
    // shape color to input color
    // start drawing to submit form
    const myModal = new bootstrap.Modal(document.getElementById('staticBackdrop'), {
        backdrop: 'static',
        keyboard: false
    });
    const shapeNameInput = document.getElementById('shapeName'); 
    const shapeColorInput = document.getElementById('shapeColor'); 
    const startDrawingButton = document.getElementById('startDrawing'); 
    let shapeOptions = {
        stroke : true,
        color : '#000000',
        fill : true,
        fillColor : '#000000',
        fillOpacity : 0.3,
        clickable : true,
    };

    // Open Street Map Tiles Layer
    const osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });
    // Google Maps Tiles Layer
    const googlemap = L.tileLayer('https://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
        maxZoom: 19,
        attribution: 'google'
    });
    
    map.zoomControl.setPosition('bottomright');

    

    
    var drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    L.control.layers({
        'osm': osm.addTo(map),
        "google": googlemap,
    }, { 'drawlayer': drawnItems }, { position: 'bottomright', collapsed: false }).addTo(map);

    // if user is not the creator of the room.
    if (missionOwner === userId){

    map.addControl(new L.Control.Draw({
        position: 'bottomright',
        edit: {
            featureGroup: drawnItems,
            remove : true,
            poly: {
                allowIntersection: false
            }
        },
        draw: {
            polyline : {
                shapeOptions : {
                    stroke : true,
                    color : shapeColorInput.value,
                }
                
            },
            polygon: {
                allowIntersection: false,
                showArea: true,
                // options
                shapeOptions : shapeOptions,
                
            },
            rectangle : false,
            circle : false,
            circlemarker : false,
        }
    })); 

    // when about to create a shape show a box that ask for shape name and shape color.
    map.on('draw:drawstart', e => {

        shapeNameInput.value  = ''; // reset shape name input
        myModal.show(); // show modal
    })

    // when start drawing, hide modal 
    // when user clicks on start drawing button
    startDrawingButton.addEventListener('click', e => {
        // hide modal and start the drawing process
        
        // if shapename input is none, error  message appear and prevent from closing
        if (shapeNameInput.value === ''){
            // prevent from closing
            alert("Shape name is required");
            
        }
        else{
            // update shape options
            shapeOptions.color = shapeColorInput.value;
            shapeOptions.fillColor = shapeColorInput.value;
            myModal.hide();
        }
    });


    // create 
    map.on('draw:created',e => {
        var layer = e.layer;
        const type = e.layerType;
        
        if(type !== 'marker'){

            layer.setStyle({
                color: shapeColorInput.value,
                fillColor: shapeColorInput.value
            });

        }

        // add shape into map, fix this part V
        //drawnItems.addLayer(layer);
        //layer.bindPopup(shapeNameInput.value,{closeOnClick: false, autoClose: false}).openPopup();
        

        const shape = layer.toGeoJSON();
        shape.properties = shapeOptions;

        // save data to database using django 
        fetch(`/save_drawing/${missionroom}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // Add CSRF token here
            },
            body: JSON.stringify({
                name: shapeNameInput.value,
                geometry: shape.geometry,
                properties : shape.properties
            }),
        })
        .then(response => response.json())
        .then(result => {
            // data is in this format {status : success, id : number}
            console.log(result);
            return fetch(`/get_one_drawing/${result.id}`)
            .then(response => response.json())
            .then(data => {
                console.log(data)
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
            })

        })
        .catch(error => {
            console.log(error);
        });

    })


    // update 
    map.on('draw:edited', e => {
        const layers = e.layers
        layers.eachLayer(layer=> {
            const shape = layer.toGeoJSON();
            const drawing_id = layer.feature.properties.drawing_id;

            fetch(`/edit_drawing/${drawing_id}`,{
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Add CSRF token here
                },
            body: JSON.stringify({
                geometry: shape.geometry,
            }),
            })
            .then(response => response.json())
            .then(result => console.log(result))
            .catch(error => console.error(error))


        });
    })
    
    // delete
    map.on('draw:deleted', e => {
        
        const layers = e.layers;
        
        layers.eachLayer(layer => {

            const drawing_id = layer.feature.properties.drawing_id;

            // fetch delete from database 
            fetch(`/delete_drawing/${drawing_id}`,{
                method : 'DELETE',
                headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'), // Add CSRF token here
            },
                body : JSON.stringify({}),
            })
            .then( response => response.json())
            .then(response => {
                console.log(response);
            })
            .catch(error => {
                console.log(error);
            })
        })
            
    })

    }

    return { map, markers, drawnItems };
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function onEachFeature(feature, layer){
    if (feature.properties && feature.properties.name) {
        layer.bindPopup(feature.properties.name,{closeOnClick: false, autoClose: false}).openPopup();
        
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