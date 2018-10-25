/**
 * Created by tedu on 2018/10/16.
 */
$(document).ready(function(){

    var seat_num ;
    var total_bill      = 0 ;
    //var pricePerTicked  = 300;//单价
    var maximumSeats    =   1;//预定座位数目的最大限制

    $('#bookNowButton').hide(); // 隐藏预定按钮

    $('.seat').each(function() {
        var column_num = parseInt( $(this).index() ) + 1;
        var row_num = parseInt( $(this).parent().index() )+1;
        seat_num = row_num+"-"+column_num ;
        $(this).text(seat_num); // 座位号
        $(this).addClass("seat"+seat_num);  // 个座位加css
    });



    // $('#seats .seat1-2').css('background-color','#71DCAA');
    // $('#seats .seat1-2').addClass('select');
    // var columnIndex = parseInt($('#seats .seat1-2').index() ) + 1;
    // var rowIndex = parseInt($('#seats .seat1-2').parent().index() )+1;
    // $("#selected_seat").append("<span class='your_selected_seat seat"+rowIndex+"-"+columnIndex+" '> " +
    //             "座位号: <b style='color:#EAABFF'>" + rowIndex+"-"+columnIndex +"</b> </br></span>");
    // $('#bookNowButton').fadeIn(1000);

    $("#seats .seat").mouseover(function(){ 
        if(!$(this).hasClass('selected')){
            $(this).css({'transform':'scale(1.3)'});
        };

    });

    $("#seats .seat").mouseleave(function(){ 
        $(this).css({'transform':'scale(1)'}); 
    });

    $("#seats .seat").click(function() {
        $('#errMsg').html('');
        $('div.comment').show();

        if(!$(this).hasClass('select')){
            $('#myModalLabel').text($(this).attr('class').split(' ')[1]+'的评论');
            $('#myModal').modal({
                show: true,
            });      
        }         
        // alert($(".your_selected_seat").length);


        if(!$(this).hasClass('selected')){
            if($(this).hasClass('select')){ // 检查是否被选中
                $(this).removeClass('select'); //如果选中了，移除选中的css
                $(this).css('background-color','rgba(255, 255, 255,0)'); // 重新加个背景
    
                var currentSeatClass = $(this).attr('class').split(' ')[1];
    
                console.log(currentSeatClass);
                $( "#selected_seat ."+currentSeatClass ).remove();
                $(".time div").remove();
    
            }else if($(".your_selected_seat").length<=maximumSeats && !$(this).hasClass('select')){

                $('#seats .seat').each(function() {   

                    if($(this).hasClass('select')){
                        console.log('12345')
                        $(this).removeClass('select');
                        $(".time div").remove();
                        $(this).css('background-color','rgba(255, 255, 255,0)'); 
                        currentSeatClass = $(this).attr('class').split(' ')[1];
                        $( "#selected_seat ."+currentSeatClass).remove();
                    }
                });

                // 检查预定的座位数目是否超出限制
                $(this).css('background-color','#71DCAA'); // 加背景颜色
                $(this).addClass("select"); // 添加选中css

                var column_num = parseInt( $(this).index() ) + 1;
                var row_num = parseInt( $(this).parent().index() )+1;
                $( "#selected_seat" ).append("<span class='your_selected_seat seat"+row_num+"-"+column_num+" '> " +
                    "座位号: <b style='color:#EAABFF'>" + row_num+"-"+column_num +"</b> </br></span>");
                $(".time").append("<div>"+"开始时间："+"<input type='time' value='06:00' id='begintime'>"+"</div>")                    
                $(".time").append("<div>"+"开始时间："+"<input type='time' value='06:00' id='endtime'>"+"</div>")                    

              
            }else {
                $('#errMsg').html('您选中的座位已经超过限制.');
            }
    
            if($(".your_selected_seat").length){
                $('#bookNowButton').fadeIn(1000);
            }else {
                $('#bookNowButton').fadeOut(1000);
            }
        }
    });
    //}
    $('#bookNowButton').click(function(){
        var textIndex = $('#selected_seat span').attr('class').split(' ')[1];
        $.post('/upload_seat/', {
            'csrfmiddlewaretoken':'{{ csrf_token }}',
            'seatid': textIndex,
            'status': 'ordered',
        });
        // alert(textIndex);
        $('#seats .'+textIndex).css('background-color','red');
        $('#seats .'+textIndex).addClass("selected")
        $('#seats .'+textIndex).removeClass("select")
        $( "#selected_seat ."+textIndex).remove();
        $('#bookNowButton').fadeOut(1000);
        $(".time div").remove();
    });
});