const Cookies = window.Cookies;
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
      setInterval(()=>{navigator.geolocation.getCurrentPosition(positionUpdate, positionError, options)}, 10000)
  } else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function positionUpdate(position) {
  showPosition(position)
  patchUserPosition(position)
}


function showPosition(position) {
  x.innerHTML = "Latitude: " + position.coords.latitude +
  "<br>Longitude: " + position.coords.longitude;
}

function patchUserPosition(position) {
  const csrftoken = Cookies.get('csrftoken');
  const req = new XMLHttpRequest();
  req.open('PATCH', 'http://127.0.0.1:8000/api/user_positions/', true);
  req.setRequestHeader("Accept", "application/json");
  req.setRequestHeader("Content-Type", "application/json");
  req.setRequestHeader("X-CSRFToken", csrftoken);
    const positions = {gps_lat:position.coords.latitude, gps_lon:position.coords.longitude};
  req.send(JSON.stringify(positions));
}




