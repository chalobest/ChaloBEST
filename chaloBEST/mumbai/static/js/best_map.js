$(function() {
    $('.listfilter_input').keyup(function() {
        var val = $(this).val();
        var $rows = $(this).parents("table").find(".listItem");
        $rows.each(function() {
            var thisTxt = $(this).text();
            //console.log(thisTxt);
            if (thisTxt.toLowerCase().indexOf(val.toLowerCase()) == -1) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    });
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

