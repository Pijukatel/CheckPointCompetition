const ol = window.ol

const element = document.getElementById('popup');

const userColors = Array.from({ length: 100 }, () => {
  return '#'+(0x1000000+(Math.random())*0xffffff).toString(16).substr(1,6);
});

let teamStyleMapping = {}

const styles = {
  'Checkpoint': new ol.style.Style({
    image: new ol.style.RegularShape({
      points: 3,
      radius: 10,
      angle: 0,
      fill: new ol.style.Fill({color: '#d71616'}),
      stroke: new ol.style.Stroke({color: '#000000', width: 1}),
    }),
  }),
  'Users': userColors.map( (color)=> {return new ol.style.Style({
      image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({color: color}),
      stroke: new ol.style.Stroke({color: '#000000', width: 1}),
    }),
  })})


};

function createBaseLayerMap() {
    const map = new ol.Map({
        target: 'map',
        layers: [
            new ol.layer.Tile({
                source: new ol.source.OSM()
            })
        ],
        view: new ol.View({
            center: ol.proj.fromLonLat([11.974560, 57.68]),
            zoom: 12
        })
    });
    const userSource = new ol.source.Vector({});
    const userLayer = new ol.layer.Vector({source: userSource,});

    const checkpointSource = new ol.source.Vector({});
    const checkpointLayer = new ol.layer.Vector({source: checkpointSource,});

    map.addLayer(userLayer);
    map.addLayer(checkpointLayer);

    const popup = new ol.Overlay({
        element: element,
        positioning: 'bottom-center',
        stopEvent: false,
    });
    map.addOverlay(popup);

    // display popup on click
    map.on('click', function (evt) {
      const feature = map.forEachFeatureAtPixel(evt.pixel, function (feature) {
        return feature;
      });
      if (feature) {
          $(element).popover('dispose');
          popup.setPosition(evt.coordinate);
          $(element).popover({
              placement: 'top',
              html: false,
              content: feature.get('name'),
          });
          $(element).popover('show');
      } else {
          $(element).popover('dispose');
      }
    });

    // change mouse cursor when over marker
    map.on('pointermove', function (e) {
      const pixel = map.getEventPixel(e.originalEvent);
      const hit = map.hasFeatureAtPixel(pixel);
      document.getElementById('map').style.cursor = hit ? 'pointer' : '';
    });
    // Close the popup when the map is moved
    map.on('movestart', function () {
      $(element).popover('dispose');
    });

    return {"checkpointSource": checkpointSource, "userSource": userSource}
}


function fullMap() {
    const sources = createBaseLayerMap()
    // Add all checkpoints to map once.
    addCheckpoints(sources.checkpointSource)

    // Periodically update user positions in map.
    setInterval(()=>{
        sources.userSource.clear()
        addUsers(sources.userSource)
    }, 5000)


}

async function addMarker(mapSource, point, markerStyle, markerText){

    //let [someResult, anotherResult] = await Promise.all([requestUsers(),requestUsers()]);
    //console.log(someResult)
        const iconFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([point.gps_lon, point.gps_lat])),
            name: markerText
        });
        iconFeature.setStyle(markerStyle);
        mapSource.addFeature(iconFeature);
}

async function addCheckpoints(mapSource) {
    let checkpoints = await requestCheckpoints();
    checkpoints.forEach( (point)=> {addMarker(mapSource, point, styles['Checkpoint'], `GPS: lon= ${point.gps_lon}, lat= ${point.gps_lon}`)})

}

async function addUsers(mapSource) {
    let [users, memberships] = await Promise.all([requestUsers(),requestMemberships()]);
    users.forEach( (point)=> {
        const team = memberships.find(membership => membership.user == point.user).team
        let style
        if (team in teamStyleMapping) {
            style = teamStyleMapping[team]
        }
        else {
            console.log(styles['Users'][Object.keys(teamStyleMapping).length])
            style = styles['Users'][Object.keys(teamStyleMapping).length]
            teamStyleMapping[team] = style
        }
        addMarker(mapSource, point, style, `Team: ${team}`)})
}







