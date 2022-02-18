const Cookies = window.Cookies;

const x = document.getElementById("positionViewer");

options = {
  enableHighAccuracy: true,
  timeout: 5000,
  maximumAge: 0
};

function userPositionWorkflow() {
  requestCheckpoints()
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
  req.open('PATCH', 'http://127.0.0.1:8000/api/user_positions/', true);
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
  req.open('GET', 'http://127.0.0.1:8000/api/user_positions/', true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}

function requestCheckpoints() {
  const req = new XMLHttpRequest();
  req.addEventListener('load', function() {
    console.log(this.responseText)
  });
  req.open('GET', 'http://127.0.0.1:8000/api/checkpoint_positions/', true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}

function requestMemberships() {
  const req = new XMLHttpRequest();
  req.addEventListener('load', function() {
    console.log(this.responseText)
  });
  req.open('GET', 'http://127.0.0.1:8000/api/memberships/', true);
  req.setRequestHeader("Accept", "application/json");
  req.send();
}