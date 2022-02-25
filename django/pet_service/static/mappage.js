$(function(){
    $.ajax({
        url: "get_gu/",
        dataType: 'json',
        success: function(msg){
            var msgKeys = Object.keys(msg)
            var msgValues = Object.values(msg)[0]
            var $gu = $("#gu")

            for (var i = 0; i < msgValues.length; i++){
                $gu.append($("<option>").val(msgValues[i]).text(msgValues[i]))
            }
        }
    })

    $('#gu').change(function(){
    // select의 개수가 1개라면
        if ($('select').length == 1){
            $.ajax({
                url: 'get_business/',
                dataType: 'json',
                success: function(msg){
                    var msgKeys = Object.keys(msg)
                    var msgValues = Object.values(msg)[0]
                    var msgId = Object.values(msg)[1]

                    $business = $("<select>").prop("id","business").append($("<option>").val(0).text('서비스 선택'))

                    for (var i = 0; i < msgValues.length; i++){
                        $business.append($("<option>").val(msgId[i]).text(msgValues[i]))
                    }
                    $("#wrapper").append($business)
                }
            })
        }
    })

    $('#wrapper').on('change', '#business', function(){
        $('#result').empty()
        gu_id = $("select[name=please] option:selected").val()
        bs_id = $(this).val()
        //console.log(gu_id)
        //console.log(bs_id)
        getInfo(gu_id, bs_id)
        getMap(gu_id, bs_id)

    })
})

function getInfo(gu_id, bs_id){
    $.ajax({
        url:'get_info',
        data: {'bs_id':bs_id,'gu_id':gu_id},
        dataType: 'json',
        success: function(msg){
            if (msg['info'].length >= 1){
                infolist = msg['info']
                var $table = $('#result')

                // column 생성
                for (var i=0; i <1; i++){
                    console.log(infolist)
                    var head_text = Object.keys(infolist[i])
                    var $tr = $("<tr>")
                    $tr.append($("<th>").text('상업명'))
                    $tr.append($("<th>").text('별점'))
                    $tr.append($("<th>").text('주소'))
                    $table.append($tr)
                }
                for (var i=0; i<infolist.length ; i++){
                    var $tr = $("<tr>")
                    var info_keys = Object.keys(infolist[i])
                    for (var j=0; j < 3; j++){
                        $tr.append($("<td>").text(infolist[i][info_keys[j]]))
                    }
                    $table.append($tr)
                }
            } else {
                var $table = $('#result')
                $table.append('없음')
            }
        }
    })

}
function getMap(gu_id, bs_id){
    $.ajax({
        url:'get_map',
        data: {'bs_id':bs_id,'gu_id':gu_id},
        dataType: 'html',
        success: function(msg){
            $('#map').empty()
            $('#map').append(msg)
        }
    })

}

document.querySelectorAll('.custom-select').forEach(setupSelector);

function setupSelector(selector) {
  selector.addEventListener('change', e => {
    console.log('changed', e.target.value)
  })

  selector.addEventListener('mousedown', e => {
    if(window.innerWidth >= 420) {// override look for non mobile
      e.preventDefault();

      const select = selector.children[0];
      const dropDown = document.createElement('ul');
      dropDown.className = "selector-options";

      [...select.children].forEach(option => {
        const dropDownOption = document.createElement('li');
        dropDownOption.textContent = option.textContent;

        dropDownOption.addEventListener('mousedown', (e) => {
          e.stopPropagation();
          select.value = option.value;
          selector.value = option.value;
          select.dispatchEvent(new Event('change'));
          selector.dispatchEvent(new Event('change'));
          dropDown.remove();
        });

        dropDown.appendChild(dropDownOption);
      });

      selector.appendChild(dropDown);

      // handle click out
      document.addEventListener('click', (e) => {
        if(!selector.contains(e.target)) {
          dropDown.remove();
        }
      });
    }
  });
}