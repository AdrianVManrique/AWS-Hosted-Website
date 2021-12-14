let map;
var myLat;
var myLong; 
function initMap() {
    if (navigator.geolocation) {
        console.log(navigator.geolocation.getCurrentPosition());
      } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
  map = new google.maps.Map(document.getElementById("map"), {
    

    center: { lat: myLat, lng: myLong},
    zoom: 8,
  });
}