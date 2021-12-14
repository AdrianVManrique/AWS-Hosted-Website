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

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: position.coords.latitude, lng: position.coords.longitude},
        zoom: 1,
      });
}