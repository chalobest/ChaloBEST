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
            if ($target.hasClass("selectedListItem")) {
                $target.find(".stopsList").hide().remove();
                $target.removeClass("selectedListItem");
                return;
            }
            $('.selectedListItem').find(".stopsList").hide().remove();
            $('.selectedListItem').removeClass("selectedListItem");
            $target.addClass("selectedListItem");
            if ($target.data("hasList")) {
                var $stopsList = $target.find(".stopsList"); 
                $stopsList.slideDown();
                return;
                /*
                var $stopsList = $target.find(".stopsList"); 
                if (!$stopsList.is(":visible")) {
                    $stopsList.slideDown();    
                } else {
                    $stopsList.slideUp();
                    $target.removeClass("selectedListItem");
                }
                return;
                */         
            } 
            var url = API_BASE + name + "/" + $target.find(".listItemText").text();
            $target.data("loading", true);
            var $loading = $('<span />').addClass("loadingSpan").text("Loading...").appendTo($target);
            $('#stopForm').remove();
            $('#formCol').empty();
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
                if (stopsWithGeom.length !== 0) {
                    jsonLayer.addFeatures(geojson_format.read(stopsGeojson));
                    var maxExtent = jsonLayer.getDataExtent();
                    map.zoomToExtent(maxExtent);                                                                
                }                
                $target.append($stopsList);
                // $target.data("hasList", true);
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
//                $('.selectedStop').removeClass("selectedStop");
//                $target.addClass("selectedStop");
                var props = $target.data("properties");
                var geom = $target.data("geometry");
                var $form = getStopForm(props, geom);
                var slug = $target.data("slug");
                if ($target.hasClass("has_point")) {
                    selectStopOnMap(slug);
                } else {
                    selectStopNotOnMap(slug);
                }
                
                $('#formCol').find("#stopForm").remove();
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
                .data("properties", props)
                .data("geometry", geom)
                .text(props.display_name)
                .appendTo($ul);
            $.isEmptyObject(geom) ? $li.addClass("no_has_point") : $li.addClass("has_point");
        });
        return $ul;
    }

    function getStopForm(stop, geom) {
    //    console.log(stop);
    //    console.log(geom);
        var lon = !$.isEmptyObject(geom) ? geom.coordinates[0] : '';
        var lat = !$.isEmptyObject(geom) ? geom.coordinates[1] : '';
        var $div = $('<div />');
        var $displayName = $('<h2 />').text(stop.display_name).appendTo($div);
        var $slug = $('<div />').addClass("stopSlug").text(stop.slug).appendTo($div);
        var $road = $("<div />").addClass("stopRoad").text("Road: " + stop.road).appendTo($div);
        var $direction = $("<div />").addClass("stopDirection").text("Direction: " + stop.direction).appendTo($div);
        var $routes = $('<div />').text("Routes: " + stop.routes).appendTo($div); 
//        var $formLabel = $("<div />").text("Edit:").appendTo($div);
        var $form = $('<form />').attr("id", "stopForm").appendTo($div);
        var $display_name_label = $('<label />').attr("for", "displayName").text("Display Name:").appendTo($form);;        
        var $display_name_input = $('<input />')
            .val(stop.display_name)
            .attr("id", "displayName")
            .blur(function() {
                $form.submit();
             })
            .appendTo($form);
        $('<br />').appendTo($form);
        var $name_mr_label = $('<label />').attr("for", "displayNameMr").text("Marathi Name:").appendTo($form);
        var $name_mr_input = $('<input />')
            .val(stop.name_mr)
            .attr("id", "displayNameMr")
            .blur(function() {
                $form.submit();
            })
            .appendTo($form);
        $('<br />').appendTo($form);
        var $alt_names_label = $('<label />').attr("for", "altNames").text("Alternative Names:").appendTo($form);
        var $alt_names_input = $('<input />')
            .val(stop.alternative_names)
            .attr("id", "altNames")
            .blur(function() {
                $form.submit();
            })
            .appendTo($form);
        $('<br />').appendTo($form);
        $('<input />').attr("type","button").val("Save")
            .click(function () {
                $form.submit();
            })
            .appendTo($form);
        var $lat_input = $('<input />').attr("type", "hidden").val(lat).attr("id", "lat").appendTo($form);
        var $lon_input = $('<input />').attr("type", "hidden").val(lon).attr("id", "lon").appendTo($form);
        $form.submit(function(e) {
            e.preventDefault();
            var oldProps = $('.selectedStop').data("properties");
            
            var geojson = {
                'type': 'Feature',
                'properties': {
                    'display_name': $display_name_input.val(),
                    'name_mr': $name_mr_input.val(),
                    'alternative_names': $alt_names_input.val()
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [parseFloat($lon_input.val()), parseFloat($lat_input.val())]
                }    
            };
            var props = $.extend(oldProps, geojson.properties);
            $('.selectedStop').data("properties", props);
            var geojsonString = JSON.stringify(geojson);
            //console.log(geojsonString);
            var url = API_BASE + "stop/" + stop.slug + "?srid=3857";
            var $postXHR = $.post(url, {'geojson': geojsonString}, function(response) {
                if (response.errors) {
                    alert("error saving");
                }
                //console.log(response);
            }, "json");
            $postXHR.fail(function(e) {
                alert('failed ' + JSON.stringify(e));
            });
        });   
        return $div;
    }

    function initMap() {
        var center = new OpenLayers.LonLat(8110203.9998955, 2170000.4068373);
        map = new OpenLayers.Map("mapCol", {
                  projection: new OpenLayers.Projection("EPSG:900913"),
                  displayProjection: new OpenLayers.Projection("EPSG:4326")
              });
        var layers = [];
//        layers[0] = new OpenLayers.Layer.OSM();

        layers[0] = new OpenLayers.Layer.OSM();
        layers[1] = new OpenLayers.Layer.Bing({
                name: "Bing Aerial",
                type: "Aerial",
                key: "AqGpO7N9ioFw3YHoPV3C8crGfJqW5YST4gGKgIOnijrUbitLlgcAS2A0M9SJrUv9",
        });
        geojson_format = new OpenLayers.Format.GeoJSON();
        //
        //yes, jsonLayer is global. Yes, I know it's wrong.
        jsonLayer = layers[2] = new OpenLayers.Layer.Vector("Bus Stops");
        map.addLayers(layers);
        jsonLayer.events.on({
           'featureselected': onFeatureSelect,
           'featureunselected': onFeatureUnselect
        });  

        map.setCenter(center, 12);
        var navigationControl = new OpenLayers.Control.Navigation({
            defaultDblClick: function(event) {
                //var xy = event.xy;
                var lonlat = map.getLonLatFromPixel(event.xy);
                var $stopForm = $('#stopForm');
                if ($stopForm.length === 0) {
                    return;
                }
                var slug = $('#formCol').find('.stopSlug').text();
                //console.log("slug", slug);
                var stop = $('.selectedStop').data("properties");
                $('.selectedStop').data("geometry", {
                    'coordinates': [lonlat.x, lonlat.y]
                });
                var hasPoint = $('.selectedStop').hasClass('has_point');
                $('#lon').val(lonlat.lon);
                $('#lat').val(lonlat.lat);
                $stopForm.submit();
                if (hasPoint) {
                    var feature = getStopFromSlug(slug);
                    feature.move(lonlat);
                } else {
                    var pt = new OpenLayers.Geometry.Point(lonlat.lon, lonlat.lat);
                    var feature = new OpenLayers.Feature.Vector(pt, stop);
                    $('.selectedStop').removeClass("no_has_point").addClass("has_point");
                    jsonLayer.addFeatures([feature]);
                    mapControl.select(feature);
                }                
                return;
            }
        });
        map.addControl(navigationControl);

        // Feature selection control
        mapControl = new OpenLayers.Control.SelectFeature(jsonLayer, {
            clickout: false,
            toggle: true
        });
        
        //map.addControl(new OpenLayers.Control.ZoomPanel());
        map.addControl(mapControl);
        mapControl.activate();

        // Add a LayerSwitcher since we now have Bing
        map.addControl(new OpenLayers.Control.LayerSwitcher());

        // Add a permalink that opens the relevant view in OSM.org in a different window
        var permalink = new OpenLayers.Control.Permalink({base: "http://www.openstreetmap.org/"});
        map.addControl(permalink);
        $(".olControlPermalink a").attr("target","_blank").html("View in OSM");

    }

    function onFeatureSelect(e) {
        //alert(arguments);
        //console.log(feature);
        // console.log(e.feature);
        var slug = e.feature.attributes.slug;
        //alert("selected " + slug);
        $('.selectedStop').removeClass("selectedStop");
        highlightStop(slug);
        var stop = e.feature.attributes;
        var geom = {
            'coordinates': [e.feature.geometry.x, e.feature.geometry.y]
        };
        var $form = getStopForm(stop, geom);
        $('#stopForm').remove();
        $('#formCol').empty();
        $('#formCol').append($form);
//        var matchedStops = $('.' + slug);
//        matchedStops.click();
//        matchedStops.addClass('highlightedStop');
             
    }

    function onFeatureUnselect(e) {
        var slug = e.feature.attributes.slug;
        //alert("unselected " + slug);
        unhighlightStop(slug);
        $('#stopForm').remove();
        $('#formCol').empty();
//        var matchedStops = $('.' + slug);
//        matchedStops.removeClass('selectedStop');      
    }

    function highlightStop(slug) {
        $('.' + slug).addClass("selectedStop");    
    }

    function unhighlightStop(slug) {
        $('.' + slug).removeClass("selectedStop");
    }

    function getStopFromSlug(slug) {
        var features = jsonLayer.features;
        var matchedLayer = false; 
        for (var i=0; i<features.length; i++) {
            var feature = features[i];
            if (feature.attributes.slug === slug) {
                matchedLayer = feature;
            }
        }
        return matchedLayer;
    }

    function selectStopNotOnMap(slug) {
        var selectedFeature = getCurrentlySelectedFeature();
        if (selectedFeature) {
            var currentSlug = selectedFeature.attributes.slug;
            unhighlightStop(slug);
            mapControl.unselect(selectedFeature);
        } else {
            $('.selectedStop').removeClass("selectedStop");
        }
        highlightStop(slug);
    }

    function selectStopOnMap(slug) {
        var feature = getStopFromSlug(slug);
        var selectedFeature = getCurrentlySelectedFeature();
        if (selectedFeature) {
            mapControl.unselect(selectedFeature);
        } else {
            $('.selectedStop').removeClass("selectedStop");
        }
        mapControl.select(feature);
        //map.setCenter(feature.geometry);
        var lonLat = new OpenLayers.LonLat(feature.geometry.x, feature.geometry.y);
        map.setCenter(lonLat);
    }

    //return currently selected feature or false
    function getCurrentlySelectedFeature() {
       var selectedFeatures = jsonLayer.selectedFeatures;
       if (selectedFeatures.length > 0) {
           return jsonLayer.selectedFeatures[0];
 //           mapControl.unselect(selectedFeature);
       } else {
           return false;
       }
                
    }

})();
