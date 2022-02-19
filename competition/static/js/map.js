const OpenLayers = window.ol
const pointStyle =
{
    cursor : "inherit",
    fillColor : "#666666",
    fillOpacity : 0.9,
    fontColor : "#000000",
    hoverFillColor : "white",
    hoverFillOpacity : 0.8,
    hoverPointRadius : 1,
    hoverPointUnit : "%",
    hoverStrokeColor : "red",
    hoverStrokeOpacity : 1,
    hoverStrokeWidth : 0.2,
    labelAlign : "cm",
    labelOutlineColor : "white",
    labelOutlineWidth : 3,
    pointRadius : 6,
    pointerEvents : "visiblePainted",
    strokeColor : "#ee9900",
    strokeDashstyle : "solid",
    strokeLinecap : "round",
    strokeOpacity : 0.3,
    strokeWidth : 1
}

function createBaseLayerMap() {
    const map = new OpenLayers.Map("map");
    map.addLayer(new OpenLayers.Layer.OSM());

    const epsg4326 =  new OpenLayers.Projection("EPSG:4326"); //WGS 1984 projection
    const projectTo = map.getProjectionObject(); //The map projection (Spherical Mercator)

    let lonLat = new OpenLayers.LonLat( 11.974560 , 57.708870 ).transform(epsg4326, projectTo);

    let zoom=12;
    map.setCenter (lonLat, zoom);
    // map.viewPortDiv.style["overflow"]="visible";
    map.viewPortDiv.style["position"]="absolute";
    map.viewPortDiv.style["z-index"]="900";

    // Define markers as "features" of the vector layer:
    const vectorLayer = new OpenLayers.Layer.Vector("Overlay");
    map.addLayer(vectorLayer);
    function featureFactory(lon, lat, style) {
        return new OpenLayers.Feature.Vector(
            new OpenLayers.Geometry.Point( lon, lat).transform(epsg4326, projectTo),
            {description:"This is the value of<br>57, 16"},
            (style));
    }
    return {"vectorLayer": vectorLayer, "featureFactory":featureFactory}

}


function fullMap() {
    const map = createBaseLayerMap()
    // Add all checkpoints to map once.
    addCheckpoints(map)

    // Periodically update user positions in map.
    //TODO add users do different layer

    //map.vectorLayer.addFeatures(map.featureFactory(12, 57.708870, pointStyle))
    //map.vectorLayer.addFeatures(map.featureFactory(12.02, 57.708870, pointStyle))

}

function addCheckpoints(map) {
    requestCheckpoints(function(checkpoints) {
        JSON.parse(checkpoints).forEach(addCheckpointToMap);
    })
    function addCheckpointToMap(checkpoint) {
        map.vectorLayer.addFeatures(map.featureFactory(checkpoint.gps_lon, checkpoint.gps_lat, pointStyle))
    }
}


