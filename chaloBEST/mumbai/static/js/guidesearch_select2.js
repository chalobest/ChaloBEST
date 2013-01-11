var isMobile = false;
$(function() {
    $('#autocomplete_all').select2({
        ajax: {
            'url': '/autocomplete/',
            dataType: 'json',
            quietMillis: 100,
            data: function(term, page) {
                return {
                    q: term,
                    page_limit: 10,
                    page: page
                }
            },
            results: function(data, page) {
                var more = data.has_next;
                return {results: data.items, more: more};
            }
        },
        formatResult: function(item) {
            return "<div><span class='itemType'>" + item.type + ": </span><span class='itemName'>" + item.title + "</span></div>"
        },
        formatSelection: function(item) {
            location.href = item.url;
            //place_geojson.properties.feature_code_name = item.name; //FIXME: please look through select2 docs and move to an onSelect type callback, but this works for now.
            return item.type + ": " + item.title;           
            //return "<div data-id='" + item.id + "'>" + item.first_name + " " + item.last_name + "</div>";
        }
    });
});
