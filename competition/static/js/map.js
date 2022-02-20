const ol = window.ol


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


