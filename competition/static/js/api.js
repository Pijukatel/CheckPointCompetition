const Cookies = window.Cookies;
const base_url = window.location.origin
const x = document.getElementById("positionViewer");

options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function userPositionWorkflow() {
  requestMemberships()
  if (!isUserLogged()) {return}
  setInterval(()=> {
    getUserPositions()
    updateUsersPosition()
  }, 5000)

}

function isUserLogged() {
  return Boolean(document.getElementById('logged_user_link'));
}

function positionError(err) {
  console.log(err);
}

function updateUsersPosition() {
  if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(patchUserPosition, positionError, options);
  }
  else {
    x.innerHTML = "Geolocation is not supported by this browser.";
  }
}

function patchUserPosition(position) {
  const csrftoken = Cookies.get('csrftoken');
  const req = new XMLHttpRequest();
  req.open('PATCH', `${base_url}/api/current_user/`, true);
  req.setRequestHeader("Accept", "application/json");
  req.setRequestHeader("Content-Type", "application/json");
  req.setRequestHeader("X-CSRFToken", csrftoken);
    const positions = {gps_lat:position.coords.latitude, gps_lon:position.coords.longitude};
  req.send(JSON.stringify(positions));
}

function getUserPositions() {
  const req = new XMLHttpRequest();
  req.addEventListener('load', function() {
    console.log(this.responseText);
});
  req.open('GET', `${base_url}/api/user_positions/`, true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}

function requestCheckpoints(callback) {
  const req = new XMLHttpRequest();
  req.addEventListener('load', function() {callback(this.responseText);});
  req.open('GET', `${base_url}/api/checkpoint_positions/`, true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}

function requestMemberships() {
  const req = new XMLHttpRequest();
  req.addEventListener('load', function() {
    console.log(this.responseText)
  });
  req.open('GET', `${base_url}/api/memberships/`, true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}