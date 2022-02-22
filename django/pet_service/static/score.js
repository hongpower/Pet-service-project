$(function(){
    if (navigator.geolocation) {
        // GeoLocation을 이용해서 접속 위치를 얻어옵니다
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude, // 위도
                lon = position.coords.longitude; // 경도
            get_myloc(lat,lon);
          });

    } else { // HTML5의 GeoLocation을 사용할 수 없을때 마커 표시 위치와 인포윈도우 내용을 설정합니다
        var locPosition = new kakao.maps.LatLng(33.450701, 126.570667),
            message = 'geolocation을 사용할수 없어요..'
    }
    $(".bs").click(function(){
        business_name = $(this).attr('id')
        user_loc = $('#user_loc').text()
        getbargraph(business_name, user_loc)
    })

})
function get_myloc(lat, lon){
    $.ajax({
        url:'get_myloc',
        data: {'lat':lat,'lon':lon},
        dataType: 'html',
        success: function(msg){
            $('h1').append(msg)
        }
    })
}
function getbargraph(business_name, user_loc){
    $.ajax({
        url:'/getbargraph/',
        data: {'business_name':business_name,'user_loc':user_loc},
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


