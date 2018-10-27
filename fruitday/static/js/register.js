/**
 * Created by tarena on 18-10-22.
 */
$(function () {
    //表示手机号是否已经被注册过的一个状态值
    // var registStatus = 1;
    window.registStatus = 1;

    /** 1.为uphone绑定blur事件*/
    $("input[name='uphone']").blur(function () {
        //如果文本框内任何东西则返回
       if($(this).val().trim().length==0)
           return;
       //如果文本框内有东西则发哦少年宫ａｊａｘ请求判断数据是否存在
       $.get(
           '/check_uphone/',
           {'uphone':$(this).val()},
           function (data) {
               $("#errshow").html(data.msg);
               //为registStatus赋值，以便提交表单时使用
               window.registStatus = data.status;
           },'json'
       );

    });
    /** 2.为　#formReg表单元素绑定submit事件*/
    $("#formReg").submit(function () {
        //判断registStatus的值判断表单是否要提交
        if(window.registStatus == 1)
            return false;
        return true;
    })
});