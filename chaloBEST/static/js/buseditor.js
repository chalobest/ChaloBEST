(function($) {
    var API_BASE = 'http://chalobest.in/1.0/';
    //console.log(API_BASE);
    var clickedName = 'stops';
    var searchQuery = 'None';
    var url1 = API_BASE + clickedName + '/' + '?q=';
    var url2 = API_BASE + clickedName + '/';
    var Features = Backbone.Model.extend({
	
	
	});

    var apiCollection = Backbone.Collection.extend({
        model: Features,
        url: searchQuery != 'None' ? url1 + searchQuery : url2,
        parse: function(response) {
            return response.features;
        }

    });
    
    var apiView = Backbone.View.extend({
        //el: '#content',
        events: {
            "click a": "clicked"
        },

        initialize: function() {
            //this.render();
            _.bindAll(this, "render", "clicked");
            this.collection.bind("all", this.render, this.clicked);
            //apiView.prototype.initialize.call(this);
        },
        render: function() {
            //$(this.el).html(this.counter = this.collection.length);
            //console.log(this.collection.length);
            //console.log(this.el);
            this.collection.each(function(model) {
                $('#sideBar').append('<li> <a id=\'' + model.cid + '\' href="#">' + model.get('properties').official_name + "</a></li>");
                //console.log(model.cid);
            });

            return this;

        },
        clicked: function(e) {
            //e.preventDefaults();
            //var name1 = this.model.get('properties').official_name;
	    	
            //console.log(e);
	    //alert("you clicked me"+ e.target.innerHTML);            
            events.trigger('stopdetailsEvent', e);
            //return this;
        },




        //close: function() {
          //  $(this.el).unbind();
           // $(this.el).remove();
        //}


    });
var stopView = Backbone.View.extend({
        el: '#content',
        initialize: function() {
            _.bindAll(this, "stopDetails");
            this.collection.bind("stopdetailsEvent", this.stopDetails);

        },

        stopDetails: function(e) {
	    //console.log(e);	
	    //alert("you clicked me"+ e.target.innerHTML);
            var cid = $(e.target).attr('id');
            //this.trigger
            //console.log(cid);
            this.values = this.collection.getByCid(cid);
            //this.trigger('new-stage', this.collection.get)
            this.stopName = e.target.innerHTML;
            //var test = this.collection.where({official_name: this.stopName});
            //console.log(this.values.get('properties').road);
	    //console.log(this.el);
            $(this.el).find('input#sLug').val(this.values.get('properties').slug);
	    //$('#sLug').attr('id', 'sLug').value(this.values.get('properties').slug);	
            $(this.el).find('input#rOads').val(this.values.get('properties').road);
            $(this.el).find('textarea#rOutes').html(this.values.get('properties').routes);
            $(this.el).find('input#dIrection').val(this.values.get('properties').direction);
            //console.log(e.target);
            $(this.el).find('input#dIsplayName').val(this.values.get('properties').official_name);
            $(this.el).find('input#mArathiName').val(this.values.get('properties').name_mr);
            $(this.el).find('input#aLtName').val(this.values.get('properties').alternative_names);
            
        },
    });	
    

        events = new apiCollection();
    $(function() {
	stopDetailsView = new stopView({
            el: $("#content"),
	    collection: events	
        });
        eventView = new apiView({
            el: $("#sideBar"),
            //el: $('#slug'),
            //el:$('#displayName'),    
            collection: events

        });
       

        events.fetch({
            success: function() {
                console.log(events.length);
                //console.log(this.official_name);
                //alert();
            }
        });
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

    //var router = Backbone.Router.extend({
    //routes:{
    //})
})(jQuery);
