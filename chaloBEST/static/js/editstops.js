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
            $.post("/" + name, {}, function(items) {
                $.each(items, function(i,v) {
                    var $li = $('<li />')
                        .addClass("listItem")
                        .text(v)
                        .appendTo($list);
                });
            }, "json");
        }

        $('.listWrapper').hide();
        $listWrapper.show();
        $('.selected').removeClass("selected");
        $that.addClass("selected");
    });

});
