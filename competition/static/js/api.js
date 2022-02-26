const Cookies = window.Cookies;
const base_url = window.location.origin
const x = document.getElementById("positionViewer");

options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function userPositionWorkflow() {
  if (!isUserLogged()) {return}
  setInterval(()=> {
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
  req.open('PATCH', `${base_url}/api/current_user_pos/`, true);
  req.setRequestHeader("Accept", "application/json");
  req.setRequestHeader("Content-Type", "application/json");
  req.setRequestHeader("X-CSRFToken", csrftoken);
    const positions = {gps_lat:position.coords.latitude, gps_lon:position.coords.longitude};
  req.send(JSON.stringify(positions));
}

function requestEndoint(endpoint) {
  const jsonData = fetch(`${base_url}${endpoint}`).then((response) => { return response.json()});
  return jsonData;
}

function requestUsers() {
  return requestEndoint("/api/user_positions/");
}

function requestCheckpoints(callback) {
  return requestEndoint("/api/checkpoint_positions/");
}

function requestMemberships() {
  return requestEndoint("/api/memberships/");
}

function requestTeams() {
  return requestEndoint("/api/teams/");
}

function requestPoints() {
  return requestEndoint("/api/points/");
}

function requestUser() {
  return requestEndoint("/api/user/");
}

function requestScore() {
  return requestEndoint("/api/score/");
}
