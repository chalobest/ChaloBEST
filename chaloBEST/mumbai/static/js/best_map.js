$(function() {
    var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{minZoom:1,maxZoom:18,attribution:'Map data © openstreetmap contributors'});
    map = new L.Map('map', {layers: [osm], center: new L.LatLng(19.04719036505186, 72.87094116210938), zoom: 11 });
});


function loadStopsGeojson(geojson) {
   jsonLayer = L.geoJson(geojson, {
        onEachFeature: function(feature, layer) {
            var url = feature.properties.url;
            layer.on("click", function(e) {
                location.href = url;
            });
            layer.on("mouseover", function(e) {
                var lon = layer.feature.geometry.coordinates[0];
                var lat = layer.feature.geometry.coordinates[1];
                //console.log(lat, lon);
                var latlng = new L.LatLng(lat, lon);
                //console.log(latlng);
                //console.log(layer.feature);
                var props = layer.feature.properties;
                var popup = L.popup({offset: new L.Point(0,-35)})
                    .setLatLng(latlng)
                    .setContent('<p>' + props.display_name + '<br>' + props.name_mr + '<br>' + props.routes + '</p>');
                map.openPopup(popup);
            });
            layer.on("mouseout", function(e) {
                map.closePopup();
            });

        }
    }).addTo(map);
}

