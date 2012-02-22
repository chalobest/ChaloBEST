var API_BASE = "/1.0/",
    map;
(function() {
    $(function() {
        initMap();
        $('.tabButton').click(function() {
            if ($(this).hasClass("selected")) {
                return;
            }
            var $that = $(this);
            var name = $that.attr("data-name");
            var $listWrapper = $('#' + name);
            if ($that.data("loaded")) {
                $.noop(); //dont load data
            } else {
                $that.data("loaded", true);
                var $list = $('#' + name + 'List');
                var url = API_BASE + name + "/";
                var $loadingLi = $('<div />').text("Loading...").appendTo($list);
                $.getJSON(url, {'srid': 3857}, function(items) {
                    $loadingLi.remove();
                    $.each(items, function(i,v) {
                        var $li = $('<div />')
                            .addClass("listItem")
                            .appendTo($list);
                        var $txt = $('<span >').addClass("listItemText").text(v).appendTo($li);
                    });
                });
            }

            $('.listWrapper').hide();
            $listWrapper.show();
            $('.selected').removeClass("selected");
            $that.addClass("selected");
        });

        $('.list').click(function(e) {
            var name = $(this).attr("id").replace("sList", ""); //FIXME: stick name in a data attr or so?
            var $target = $(e.target).parent();
            if (!$target.hasClass('listItem')) {
                return;
            }
            if ($target.data("loading")) {
                return;
            }
            $('.selectedListItem').removeClass("selectedListItem");
            $target.addClass("selectedListItem");
            if ($target.data("hasList")) {
                $target.find(".stopsList").toggle();
                return;         
            } 
            var url = API_BASE + name + "/" + $target.find(".listItemText").text();
            $target.data("loading", true);
            var $loading = $('<span />').addClass("loadingSpan").text("Loading...").appendTo($target);
            $.getJSON(url, {'srid': 3857}, function(obj) {
                $loading.remove();
                var stopsGeojson = obj.stops;              
                var stops = stopsGeojson.features;
                var $stopsList = getStopsList(stops);
                var stopsWithGeom = [];
                $.each(stops, function(i,v) {
                    if (!$.isEmptyObject(v.geometry)) {
                        stopsWithGeom.push(v);
                    }    
                });
                stopsGeojson.features = stopsWithGeom;
                var currFeatures = jsonLayer.features;
                jsonLayer.removeFeatures(currFeatures);
                jsonLayer.addFeatures(geojson_format.read(stopsGeojson));
                var maxExtent = jsonLayer.getDataExtent();
                map.zoomToExtent(maxExtent);                
                $target.append($stopsList);
                $target.data("hasList", true);
                $target.data("loading", false);
            });
        });

        $('.listSearch').keyup(function(e) {
            var val = $(this).val();
            var name = $(this).attr("id").replace("Search", "");
            var $list = $('#' + name + "List");
            $list.find(".listItem").each(function() {
                var $that = $(this);
                var txt = $that.find(".listItemText").text();
                if (txt.indexOf(val) == -1) {
                    $that.hide();
                } else {
                    $that.show();
                }
            });
        });

    });

    function getStopsList(stops) {
        var $ul = $('<ul />')
            .addClass("stopsList")
            .click(function(e) {
                var $target = $(e.target);
                if ($target.hasClass("selectedStop")) {
                    return;
                }
                $('.selectedStop').removeClass("selectedStop");
                $target.addClass("selectedStop");
                var props = $target.data("properties");
                var $form = getStopForm(props);
                $('#formCol').empty();
                $('#formCol').append($form);
            });

        $.each(stops, function(i,v) {
            var props = v.properties;
            var geom = v.geometry;
            var $li = $('<li />')
                .addClass("stopItem")
                .data("slug", props.slug)
                .addClass(props.slug) //FIXME: please dont set data AND addClass AND include slug in properties.
                .data("properties", props).data("geometry", geom)
                .text(props.display_name)
                .hover(function() {
                   //TODO: when hover over a stop name in list, it should set some styleMap stuff on the map to colour the moused-over location. 
                }, function() {
    
                })
                .appendTo($ul);
            $.isEmptyObject(geom) ? $li.addClass("no_has_point") : $li.addClass("has_point");
        });
        return $ul;
    }

    function getStopForm(stop) {
    //    console.log(stop);
        var $div = $('<div />');
        var $displayName = $('<div />').text(stop.display_name).appendTo($div);
        var $routes = $('<div />').text("Routes: " + stop.routes).appendTo($div); 
    //    var $form = $('<form />').apendTo($div);    
        return $div;
    }

    function initMap() {
        var center = new OpenLayers.LonLat(8110203.9998955, 2170000.4068373);
        map = new OpenLayers.Map("mapCol", {
                  projection: new OpenLayers.Projection("EPSG:900913")
              });
        var layers = [];
//        layers[0] = new OpenLayers.Layer.OSM();

        layers[0] = new OpenLayers.Layer.OSM();
        geojson_format = new OpenLayers.Format.GeoJSON();
        //yes, jsonLayer is global. Yes, I know it's wrong.
        jsonLayer = layers[1] = new OpenLayers.Layer.Vector({
                geometryType: 'Point',
                projection: new OpenLayers.Projection("EPSG:4326")
                });
        //  map.addLayer(vector_layer);
        map.addLayers(layers);
        map.setCenter(center, 12);

        mapControl = new OpenLayers.Control.SelectFeature(layers[1]);
        zoomControl = new OpenLayers.Control.ZoomToMaxExtent();
        map.addControl(mapControl);
        //  map.addControl(zoomControl);
        mapControl.activate();
        //  zoomControl.activate();
        layers[1].events.on({
           'featureselected': onFeatureSelect,
           'featureunselected': onFeatureUnselect
        });  
    }

    function onFeatureSelect(feature) {
        var slug = feature.attributes.slug;
        alert("selected " + slug);
        var matchedStops = $('.' + slug);
        matchedStops.addClass('highlightedStop');      
    }

    function onFeatureUnselect(feature) {
        var slug = feature.attributes.slug;
        alert("unselected " + slug);
        var matchedStops = $('.' + slug);
        matchedStops.removeClass('highlightedStop');      
    }

})();