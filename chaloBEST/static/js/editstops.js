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
                        .text(v)
                        .appendTo($list);
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
        var $target = $(e.target);
        if (!$target.hasClass('listItem')) {
            return;
        }
        if ($target.data("loading")) {
            return;
        }
        if ($target.data("hasList")) {
            $target.find(".stopList").toggle();
            return;         
        } 
        var url = API_BASE + name + "/" + $target.text();
        $target.data("loading", true);
        var $loading = $('<span />').addClass("loadingSpan").text("Loading...").appendTo($target);
        $.getJSON(url, {}, function(area) {
            $loading.remove();
            var stops = area.stops.features;
            var $stopsList = getStopsList(stops);
            $target.append($stopsList);
            $target.data("hasList", true);
            $target.data("loading", false);
        });
    });

});

function getStopsList(stops) {
    var $ul = $('<ul />').addClass("stopsList");
    $.each(stops, function(i,v) {
        var props = v.properties;
        var geom = v.geometry;
        var $li = $('<li />').addClass("stopItem").data("slug", props.slug).data("geometry", geom).text(props.display_name).appendTo($ul);
    });
    return $ul;
}
