let map;
var myLat;
var myLong; 
function initMap() {
    if (navigator.geolocation) {
        console.log("I AM GETTING COORDS");
        navigator.geolocation.getCurrentPosition(setPosition);
      } else {
        x.innerHTML = "Geolocation is not supported by this browser.";
      }
  map = new google.maps.Map(document.getElementById("map"), {
    

    center: { lat: myLat, lng: myLong},
    zoom: 8,
  });
}

function setPosition(position){
    myLat = position.coords.latitude;
    myLong = position.coords.longitude;
    parseFloat(myLat);
    parseFloat(myLong);
    console.log(myLat);
    console.log(myLong);
}