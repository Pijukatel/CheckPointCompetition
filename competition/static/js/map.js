const ol = window.ol

const element = document.getElementById('popup');

const styles = {
  'Checkpoint': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({color: '#d71616'}),
      stroke: new ol.style.Stroke({color: '#000000', width: 1}),
    }),
  }),
  'User': new ol.style.Style({
    image: new ol.style.Circle({
      radius: 5,
      fill: new ol.style.Fill({color: '#d7d416'}),
      stroke: new ol.style.Stroke({color: '#000000', width: 1}),
    }),
  })

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
        popup.setPosition(evt.coordinate);
        $(element).popover({
          placement: 'top',
          html: true,
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
    //TODO add users do different layer
    setInterval(()=>{
        sources.userSource.clear()
        addUsers(sources.userSource)
    }, 5000)





}

function addMarker(mapSource, markerStyle, requestCallback){
     requestCallback(function(point) {
        JSON.parse(point).forEach(addPointToMap);
    })

    function addPointToMap(point) {
        const iconFeature = new ol.Feature({
            geometry: new ol.geom.Point(ol.proj.fromLonLat([point.gps_lon, point.gps_lat])),
            name: 'Whatever'
        });
        iconFeature.setStyle(markerStyle);
        mapSource.addFeature(iconFeature);
    }
}

function addCheckpoints(mapSource) {
    addMarker(mapSource, styles['Checkpoint'], requestCheckpoints)
}

function addUsers(mapSource) {
    addMarker(mapSource, styles['User'], requestUsers)
}







