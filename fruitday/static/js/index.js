/**
 * Created by tarena on 18-10-22.
 */
	$(function(){
		var $addr = $('.address>span');

		var $add1 = $('.select>li:first');
		var $add2 = $('.select>li:odd');
		var $add3 = $('.select>li:last');


		$add1.bind('click',function(){

			$addr.text($add1.text());
		});

		$add2.bind('click',function(){

			$addr.text($add2.text());

		});

		$add3.bind('click',function(){

			$addr.text($add3.text());

		});

		var banner = document.getElementsByClassName('wrapper')[0];
		var imgs = banner.children; //图片数组
		var imgNav = document.getElementsByClassName('imgNav')[0];
		var indInfo = imgNav.children; //索引数组
		var imgIndex = 0; //初始下标
		var timer;
		timer = setInterval(autoPlay,2000);
		function autoPlay(){
			//设置元素影藏与现实
			imgs[imgIndex].style.display = "none";
			// ++ imgIndex;
			// if(imgIndex == img.length){
			// 	imgIndex = 0;
			// }
			imgIndex = ++ imgIndex == imgs.length ? 0 : imgIndex;
			imgs[imgIndex].style.display = "block";

			for (var i = 0; i < indInfo.length; i++) {
				indInfo[i].style.background = "gray";
			}

			// 切换索引，切换背景色
			indInfo[imgIndex].style.background = "orange";
		}
		banner.onmouseover = function(){
			// 停止定时器
			clearInterval(timer);
		};
		banner.onmouseout = function(){
			timer = setInterval(autoPlay,2000);
		};


	});

function check_login() {
    //向 /check_login/ 发送异步请求
    $.get('/check_login/',function (data) {
        var html = "";
        if(data.loginStatus == 0){
            html += "<a href='/login'>[登录]</a>";
            html += "<a href='/register'>[注册,有惊喜]</a>";
        }else{
            html += "欢迎:"+data.uname;
            html += "<a href='/logout/'>退出</a>"
        }
        $("#login").html(html);
    },'json');
}

function cart_check() {
	$.get('/check_login',function (data) {
		var html = "";
		if(data.loginStatus == 1){
			html += "<a href='/cart'>购物车</a>";
		}else {
			html += "<a href='/'>购物车</a>";
		}
		$("#car").html(html)
    },'json');
}

/**加载所有的商品分类以及商品信息(每个分类取钱10个)*/
function loadGoods() {
	$.get('/load_type_goods/',function (data) {
		//data就是响应回来的JSON对象
		var show = "";
		$.each(data,function (i,obj) {
			//从obj中取出type,并转换为json对象
			var jsonType = JSON.parse(obj.type);
			//加载type的信息
			show += "<div class='item' style='overflow: hidden;'>";
			  show += "<p class='goodsClass'>";
			    show += "<img src='/"+jsonType.picture+"'>";
			    show += "<a href='#'>更多</a>";
			  show += "</p>";
			  //加载ul以及li们
			  show += "<ul>";
			    var jsonGoods = JSON.parse(obj.goods);
			    $.each(jsonGoods,function (i,good) {
					//创建li
					show += "<li ";
					if ((i+1) % 5==0){
						show += "class='no-margin'";
					}
					show += ">";
					  //拼p标记,表示商品的图片
					  show += "<p>";
					    show += "<img src='/"+good.fields.pictrue+"'>";
					  show += "</p>";
					  //拼div标记,表示的是商品详细的描述
					  show += "<div class='content'>";
					    show += "<a href='javascript:add_cart("+good.pk+");'>";
					      show += "<img src='/static/img/cart.png'>";
					    show += "</a>";
					    show += "<p>"+good.fields.title+"</p>";
					    show += "<span>";
					      show += "&yen;"+good.fields.price+"/"+good.fields.spec;
					    show += "</span>";
					  show += "</div>";
					show += "</li>";
                });
			  show += "</ul>";
			show += "</div>";
        });
		$("#main").html(show);
    },'json')
}


/** 添加商品到购物车 gid: 表示要添加到购物车的商品id*/
function add_cart(gid) {
	//1.验证登录账户，如果没有用户登录的话则给出相应的提示
	$.get('/check_login/',function (data) {
		if(data.loginStatus == 0){
		    alert('请登录在购买商品')
		}else{
			$.get('/add_cart/',
				{'gid':gid},
			function (data) {
				if(data.status == 1){
					alert(data.statusText);
				}else{
					alert("添加购物车失败")
				}
            },'json');
		}
    },'json');
	//2.有登录则添加到购物车
}

$(function () {
   /**调用check_login检查登录状态*/
   check_login();
   /** 调用loadGoods函数得到所有的类型和商品*/
   loadGoods();
   /** 调用cart_check函数获得进入购物车权限*/
   cart_check();
});
