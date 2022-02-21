$(function(){
    $(".bs").click(function(){
        business_name = $(this).attr('id')
        getScore(business_name)
    })
    $("#plz").click(function(){
        getPie()
    })
})

function getScore(business_name){
    $.ajax({
        url:'/getscore/',
        data: {'business_name':business_name},
        dataType:'html',
        cache: false,
        success: function(msg){
            $('.container').empty()
            $('.container').html('<img src="data:image/png;base64,'+msg+'">')
        }
    })
}
function getPie(){
    $.ajax({
        url:'/getpie/',
        dataType: 'html',
        cache: false,
        success: function(msg){
            $('#pie').empty()
            $('#pie').html('<img src="data:image/png;base64,'+msg+'">')
        }
    })
}


