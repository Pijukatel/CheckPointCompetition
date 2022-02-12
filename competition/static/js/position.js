
function positionError(err) {
  console.log(err);
}


options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

const x = document.getElementById("positionViewer");

function getLocation() {
  if (navigator.geolocation) {
      setInterval(()=>{navigator.geolocation.getCurrentPosition(showPosition, positionError, options)}, 1000)
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function showPosition(position) {
  x.innerHTML = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;
}
