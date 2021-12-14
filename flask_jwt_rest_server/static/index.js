let map;
let markers = [];

function initMap() {
  if (navigator.geolocation) {
    console.log("I AM GETTING COORDS");
    navigator.geolocation.getCurrentPosition(setPosition);
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function setPosition(position) {
  const myLatlng = { lat: position.coords.latitude, lng: position.coords.longitude };
  map = new google.maps.Map(document.getElementById("map"), {
    center: myLatlng,
    zoom: 15,
  });

  // Create the initial InfoWindow.
  let infoWindow = new google.maps.InfoWindow({
    content: "This is your location",
    position: myLatlng,
  });

  infoWindow.open(map);
  // Configure the click listener.
  google.maps.event.addListener(map, "click", (event) => {
    // Close the current InfoWindow.
    infoWindow.close();

    document
      .getElementById("delete-markers")
      .addEventListener("click", deleteMarkers);

    addMarker(event.latLng, map);


  });
}

function addMarker(location, map) {
  // Add the marker at the clicked location, and add the next-available label
  // from the array of alphabetical characters.
  const marker = new google.maps.Marker({
    position: location,
    map: map,
  });

  markers.push(marker);
}

function setMapOnAll(map) {
  for (let i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}


function deleteMarkers() {
  setMapOnAll(null);
  markers = [];
}