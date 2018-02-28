/**
 * Created by python on 17-8-23.
 */

   var in1_ok = false;
   var in2_ok = false;
   var in3_ok = false;
   var in4_ok = false;
   var in5_ok = false;
   var in2_cut;
   $(function () {
            // 默认进来将读取到的表格名称get到后台来查询表格中的sheet

            //--------------------默认分割线---------------------
            $('.in1').blur(function () {
                var len= $('.in1').val().length;
                if(len==0)
                {
                    $('.in1').prev().html('输入内容不能为空').show();
                    in1_ok=false;
                }
                else
                {
                    $('.in1').prev().html('&nbsp;').show();
                    in1_ok=true;
                }
            });
            $('.in2').blur(function () {
                var len=$('.in2').val().length;
                if(len==0)
                {
                    $('.in2').prev().html('输入内容不能为空').show();
                    in2_ok=false;
                }
                else
                {
                    in2_cut = $('.in2').val().split('_')[0];
                    if(in2_cut == 'nlu' || in2_cut == 'nlp' || in2_cut == 'pstt' || in2_cut == 'asr')
                    {
                        $.get('/caseid_valid/',{'tablename':$('.in3').val(),'caseid':$(this).val()},function (data) {
                        if(data.result == 0)
                        {
                            $('.in2').prev().html('表格中无此用例ID').show();
                            in2_ok=false;
                        }
                        else
                        {
                            $('.url_text').hide();
                            $('.add').hide();
                            $('.minus').hide();
                            $('.in2').prev().html('&nbsp;').show();
                            in2_ok=true;
                        }
                    });
                    }
                    else
                    {
                        $('.in2').prev().html('输入格式不正确').show();
                        in2_ok=false;
                    }
                }
            });

            $('.in3').blur(function () {
                var len=$('.in3').val().length;
                if(len==0)
                {
                    $('.in3').prev().html('输入内容不能为空').show();
                    in3_ok=false;
                    $('.in2').attr('disabled','disable')
                }
                else
                {
                    $.get('/table_valid/',{'tablename':$(this).val()},function (data) {
                        if(data.result == 0)
                        {
                            $('.in3').prev().html('表格不存在,请上传后重试').show();
                            in3_ok=false;
                            $('.in2').attr('disabled','disable')
                        }
                        else
                        {
                            $('.in3').prev().html('&nbsp;').show();
                            in3_ok=true;
                            $('.in2').removeAttr('disabled');
                            var table_name = $(".table_name:selected").val();
                            $.get("/sheet_valid/",{"table_name":table_name},function (data) {
                                $(".in6").children().remove();
                                // $(".in6").append("<option value='sheet_all'>sheet_all</option>>");
                                $.each(data.result, function (index,value) {
                                    $(".in6").append("<option value=" + value + ">" + value + "</option>>")
                                });
                            });
                        }
                    });
                }
            });
            $('.in4').blur(function () {
                var len=$('.in4').val().length;
                if(len==0)
                {
                    $('.in4').prev().html('输入内容不能为空').show();
                    in4_ok=false;
                }
                else
                {
                    $('.in4').prev().html('&nbsp;').show();
                    in4_ok=true;
                }
            });

            $('.url_text').delegate('input','blur',function(){
                    var len=$(this).val().length;
                    if(len==0)
                    {
                        $('.inp_error1').html('需要重启tomcat的时候,url地址不能为空').show();
                        in5_ok=false;
                    }
                    else
                    {
                        $('.inp_error1').html('&nbsp;').show();
                        in5_ok=true;
                    }
                });
            $('.add').click(function () {
                    var i=$('.in5');
                    var len=i.length;
                    if(len<6){
                        $('.url_text').append('<br><br><input type="text" class="in5" name="url" >')
                    }
                });
            $('.minus').click(function () {
                    var i=$('.in5');
                    var len=i.length;
                    if(len>1){
                         $('.url_text').children().last('input').remove();
                         $('.url_text').children().last('br').remove();
                    }
                });
            $('.reg_form').submit(function() {
                if (in2_cut == 'asr') {
                    if (in1_ok == true && in2_ok == true && in3_ok == true && in4_ok == true && in5_ok == true) {
                        alert("测试进行中,可到测试任务管理界面查看进行状态");
                        return true;
                    }
                    else {
                        return false;
                    }
                }
                else if (in2_cut == 'nlu' || in2_cut == 'nlp' || in2_cut == 'pstt') {
                    if (in1_ok == true && in2_ok == true && in3_ok == true && in4_ok == true) {
                        alert("测试进行中,可到测试任务管理界面查看进行状态");
                        return true;
                    }
                    else {
                        return false;
                    }
                }
                else {
                    return false;
                }
            });
        });