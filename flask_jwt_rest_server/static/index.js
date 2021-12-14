let map;
function initMap() {
    if (navigator.geolocation) {
        console.log("I AM GETTING COORDS");
        navigator.geolocation.getCurrentPosition(setPosition);
      } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
}

function setPosition(position){
    const myLatlng = { lat: 0.00, lng: 131.044 };
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: position.coords.latitude, lng: position.coords.longitude},
        zoom: 15,
      });

    // Create the initial InfoWindow.
    let infoWindow = new google.maps.InfoWindow({
        content: "Click the map to get Lat/Lng!",
        position: myLatlng,
    });

    infoWindow.open(map);
    // Configure the click listener.
    map.addListener("click", (mapsMouseEvent) => {
        // Close the current InfoWindow.
        infoWindow.close();
        // Create a new InfoWindow.
        infoWindow = new google.maps.InfoWindow({
        position: mapsMouseEvent.latLng,
        });
        infoWindow.setContent(
        JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)
        );
        infoWindow.open(map);
    });
}