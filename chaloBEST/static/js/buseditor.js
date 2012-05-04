(function($) {
    var API_BASE = 'http://chalobest.in/1.0/';
    console.log(API_BASE);
    var testName = 'stops';
    var searchQuery = 'None';
    var url1 = API_BASE + testName + '/' + '?q=';
    var url2 = API_BASE + testName + '/';
    var Features = Backbone.Model.extend({});

    var apiCollection = Backbone.Collection.extend({
        model: Features,
        url: searchQuery != 'None' ? url1 + searchQuery : url2,
        parse: function(response) {
            return response.features;
        }

    });
    var apiView = Backbone.View.extend({
        el: $('#sideBar'),
	

        initialize: function() {

            _.bindAll(this, "render");
            this.collection.bind("all", this.render);
            //apiView.prototype.initialize.call(this);
        },
        render: function() {
            $(this.el).html(this.counter = this.collection.length);
	    console.log(this.collection.length);
	    this.collection.each( function(model){
      		console.log(model.get('properties'));
		//alert(this.el);
		$('#sideBar').append("<li>" + model.get('properties').official_name + "</li>");
		//$('#sideBar').append("<li>" + model.get('properties').area + "</li>");

    	     });

	    //for(i=0; i< this.collection.length; i++) {
	   // console.log(model.get('official_name')));
	   // }
	   // $(this.el).append("<li>" + this.properties.official_name + "</li>");
            // $(this.el).html(this.template(this.model.toJSON()));
            // $(this.el).html(this.counter = this.model.toJSON());

            return this;

        }

    }),
        events = new apiCollection(),
        eventView = new apiView({

            collection: events

        });
    events.fetch({
        success: function() {
            console.log(events.length);
            //console.log(this.official_name);
            //alert();

        }
    });
   



        var Map = Backbone.Model.extend({});


        var MapView = Backbone.View.extend({
            el: '#mapCol',

            initialize: function() {
                _.bindAll(this, 'initMap');
                this.initMap();

            },

            initMap: function() {
                // Initialize Basic Openlayers;
                var center = new OpenLayers.LonLat(8110203.9998955, 2170000.4068373);
                //alert("you are here");
                map = new OpenLayers.Map(this.el, {
                    projection: new OpenLayers.Projection("EPSG:900913"),
                    displayProjection: new OpenLayers.Projection("EPSG:4326")
                });
                //alert(this.el);
                var layers = [];
                layers[0] = new OpenLayers.Layer.OSM(); //some more layer will go here
                //$(this.el).html(map);           
                map.addLayers(layers);
                map.setCenter(center, 12);

            }
        });
        $(function() {
            var map_view = new MapView();
            //alert("I am here" + this.el);
        });



    })(jQuery);
