jq(function(){
    jq('.favorite').each(function(){
        if(!jq('#regio-content').hasClass('documentEditable')){
            jq(this).children('.portletItem').each(function(){
                if(!jq(this).hasClass('portletItemEmpty')){
                    jq(this).append('<a class="close favoriteRemove" title="entfernen"><img alt="remove" src = "'+portal_url+'/++resource++icon_remove_box.gif"/></a>')
                }
            });
        }
    });


    //Remove Favorite
    jq('.favoriteRemove').click(function(e){
        e.stopPropagation();
        e.preventDefault();
        var item = jq(this).closest('.favorite');
        var uid = item.attr("id");
        jq.ajax({
            type :      'POST',
            url :       './remove_from_favorites',
            data :      'uid='.concat(uid)
        });
        
        item.hide().remove();
    });
  
});