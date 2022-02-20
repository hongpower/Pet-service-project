$(function(){
    $(".bs").click(function(){
//        alert('클릭')
//        console.log($(this).attr('id'))
        business_name = $(this).attr('id')
        getScore(business_name)
//        $('.container').empty()
//        alert('클릭')

    })
    $("#pie").click(function(){
        getPie()
    })
})
cnt = 0
function getScore(business_name){
    $.ajax({
        url:'/getscore/',
        data: {'business_name':business_name},
        dataType:'html',
        success: function(msg){
            $('.container').empty()
            console.log(msg)
            var img = $('<img>').prop('src', msg)
            img.appendTo('.container')
//            $('.container').html('<img src="data:image/png;base64,'+msg+'">')
//            uri = encodeURI(msg)

//            $('img').property('src',"data:image/png;base64, ${uri}")
//            $('.container').html(uri)
        }
    })
}
// 여기 미완성!
// function getPie(){
//     $.ajax({
//         url:'/getscore/',
//         data: {'business_name':business_name},
//         dataType:'html',
//         success: function(msg){
//             $('.container').empty()
//             console.log(msg)
//             var img = $('<img>').prop('src', msg)
//             img.appendTo('.container')

