var API_BASE = "/1.0/"
$(function() {
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
            $.getJSON(url, {}, function(items) {
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
        $.getJSON(url, {}, function(obj) {
            $loading.remove();
            var stopsGeojson = obj.stops; //TODO: render filtered geojson with known geometries on map
            var stops = stopsGeojson.features;
            var $stopsList = getStopsList(stops);
            $target.append($stopsList);
            $target.data("hasList", true);
            $target.data("loading", false);
        });
    });

    $('.listSearch').keydown(function(e) {
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
    var $ul = $('<ul />').addClass("stopsList").click(function(e) {
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
        var $li = $('<li />').addClass("stopItem").data("slug", props.slug).data("properties", props).data("geometry", geom).text(props.display_name).appendTo($ul);
    });
    return $ul;
}

function getStopForm(stop) {
    var $div = $('<div />');
    var $displayName = $('<div />').text(stop.display_name).appendTo($div);
    
}
