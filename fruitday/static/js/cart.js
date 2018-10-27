// /**
//  * Created by tarena on 18-8-3.
//  */

$(function(){
  //检查登录状态
  check_login();
});

/**
 * 异步向服务器发送请求，检查用户是否处于登录状态
 * */
function check_login(){
  $.get('/check_login/',function(data){
    var html = "";
    if(data.loginStatus == 0){
      html += "<a href='/login/'>[登录]</a>,";
      html += "<a href='/register/'>[注册有惊喜]</a>";
    }else{
      html += "欢迎："+data.uname;
      html += "<a href='/logout/'>退出</a>";
    }
    $("#login").html(html);
  },'json');
}
