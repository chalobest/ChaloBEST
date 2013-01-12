var isMobile = true;

$(function() {   
        
    $('.closeLightBox').click(function(event){
        event.preventDefault();
        $('.overlay').hide(300);
        $(window).unbind("resize");            
    });
    
    $('.overlay').click(function(){ 
        $('.overlay').hide(300);   
        $(window).unbind("resize");         
    });
    
    $('.lightBox').click(function(event){
        event.stopPropagation();  
    });
    

    $('#mobileGo').click(function(e) {
        e.preventDefault();
        var q = $('#autocomplete_all').val();
        var url = "/autocomplete/";
        $('#lightboxContent').html("Loading...");
        $('.overlay').show(300, function(){
            $(window).resize(function() {
    
                if ($(window).height() < $('.lightBox').height())
                {            
                    $('.overlay').css({'position':'absolute', 'height':'auto'});
                } else {
                    $('.overlay').css({'position':'', 'height':''});
                }            
            });

            $(window).resize();
        });           
        $.getJSON(url, {'q': q}, function(data) {
            //console.log(data);
            $('#lightboxContent').empty();
            var $ul = $('<ul />').addClass("searchResults").appendTo("#lightboxContent");
            for (var i=0; i<data.items.length; i++) {
                var item = data.items[i];
                var $row = getRow(item).appendTo($ul);
                $row.appendTo($ul);
            }
        });
    });

    function getRow(item) {
        var $li = $('<li />').addClass("resultItem");
        var $a = $('<a />').attr("href", item.url).appendTo($li);
        var resultText = item.type + ": " + item.title;
        var $content = $("<div />").addClass("resultContent").html(resultText).appendTo($a);
        return $li;
    }
});
