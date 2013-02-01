//var gotPosition = false;
var currentRequest = false;
$(function() {
    var osmUrl = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    var osmAttrib = 'Map data © openstreetmap contributors'
    var osm = new L.TileLayer(osmUrl, {minZoom:1,maxZoom:18,attribution: osmAttrib});
    map = new L.Map('map', {layers: [osm], center: new L.LatLng(19.04719036505186, 72.87094116210938), zoom: 11 });
    //console.log(map);
    if (!isMobile && $(window).width() < 700) { // dont show minimap on mobiles
        var osm2 = new L.TileLayer(osmUrl, {minZoom: 0, maxZoom: 13, attribution: osmAttrib});
        var miniMap = new L.Control.MiniMap(osm2).addTo(map);
    }
//    var miniMap = new L.Control.MiniMap(osm).addTo(map);
    var initialBBox = map.getBounds();
//Get user current location
    navigator.geolocation.getCurrentPosition(function(loc) {
        //on success load stops near user's latlng
        var coords = loc.coords;
        var latlng = new L.LatLng(coords.latitude, coords.longitude);
        if (initialBBox.contains(latlng)) {
//        map.setView(latlng, 15);
            loadStops(latlng);
        }
    }, function(err) {
        //if user denies location info, load stops for center point 
        var center = map.getCenter();
        loadStops(center);
    });


    map.on("moveend", function(e) {
        //if user moves map, get stops for new center
        var latlng = map.getCenter();
        loadStops(latlng);
    });


    map.fire("moveend");

});

//Load stops near latlng and render on map
function loadStops(latlng) {

    map.setView(latlng, 15);
    var url = "/1.0/stops_near/";
    var params = {
        'center_lat': latlng.lat,
        'center_lon': latlng.lng
    };
    if (currentRequest && currentRequest.readystate != 4) {
        currentRequest.abort();
    }  
    currentRequest = $.getJSON(url, params, function(data) {
        if (typeof(jsonLayer) != 'undefined') map.removeLayer(jsonLayer);
        showStopsData(data);
        
        loadStopsGeojson(data); //defined in best_map.js
     });
    
   
}

function showStopsData(data) {
    $('.stopRow').remove();
    $.each(data.features, function(i, v) {
        var props = v.properties;
        //console.log(props);
        var rowHTML = tmpl('stopTemplate', {'stop': props});
        //console.log(rowHTML);
        $('#nearStopsTable').append(rowHTML);
    });    
}

// Simple JavaScript Templating
// John Resig - http://ejohn.org/ - MIT Licensed
(function(){
  var cache = {};
  
  this.tmpl = function tmpl(str, data){
    // Figure out if we're getting a template, or if we need to
    // load the template - and be sure to cache the result.
    var fn = !/\W/.test(str) ?
      cache[str] = cache[str] ||
        tmpl(document.getElementById(str).innerHTML) :
      
      // Generate a reusable function that will serve as a template
      // generator (and which will be cached).
      new Function("obj",
        "var p=[],print=function(){p.push.apply(p,arguments);};" +
        
        // Introduce the data as local variables using with(){}
        "with(obj){p.push('" +
        
        // Convert the template into pure JavaScript
        str
          .replace(/[\r\t\n]/g, " ")
          .split("<%").join("\t")
          .replace(/((^|%>)[^\t]*)'/g, "$1\r")
          .replace(/\t=(.*?)%>/g, "',$1,'")
          .split("\t").join("');")
          .split("%>").join("p.push('")
          .split("\r").join("\\'")
      + "');}return p.join('');");
    
    // Provide some basic currying to the user
    return data ? fn( data ) : fn;
  };
})();
