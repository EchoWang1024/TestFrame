/**
 * Created by python on 17-9-14.
 */
    var input_ok =false;

    $(function () {
            //验证邮箱不能为空
            $('body').mouseout(function () {
                    var mailval = $('.mail').val();
                    var nameval = $('.name').val();
                    if((mailval == '' && nameval == '')||(mailval != '' && nameval == '姓名')||
                        (mailval == '邮箱地址' && nameval != '')||(mailval == '邮箱地址' && nameval == '姓名')
                        ||(mailval == '' && nameval == '姓名')||(mailval == '邮箱地址' && nameval == '')
                        ||(mailval != '' && nameval == '')||(mailval == '' && nameval != ''))
                    {
                        $('.errorinfo').html('输入邮箱地址和名字不能为空').show();
                         input_ok =false;
                    }
                    else
                    {
                        $('.errorinfo').html(' ').show();
                         input_ok =true;
                    }
            });
            // 加减号
            $('.add').click(function () {
                    var i=$('.mail');
                    var len=i.length;
                    if(len<7){
                        $('.first').append('<input type="text" class="mail" name="mailsite" ><br><br>')
                    }
                });
            $('.minus').click(function () {
                    var i=$('.mail');
                    var len=i.length;
                    if(len>1){
                         $('.first').children().last('.mail').remove();
                         $('.first').children().last('br').remove();
                         $('.first').children().last('br').remove();
                    }
                });
            //submit提交事件
            $('form').submit(function () {
                if(input_ok == true)
                {
                    return true
                }
                else
                {
                    return false
                }
            })
        });