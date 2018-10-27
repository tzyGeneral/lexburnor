import json

from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def login_views(request):
    #判断是get请求还是post请求
    if request.method == 'GET':
        #1.获取来访地址，如果没有则设置为/
        url = request.META.get('HTTP_REFERER','/')
        #get请求　－判断session,判断cookie，登录页
        #判断session中是否有登录信息
        if 'uid' in request.session and 'uphone' in request.session:
            #有登录信息在session
            #从哪里来回哪里去
            resp = HttpResponseRedirect(url)
            return resp
        else:
            #没有登录信息保存在session,判断cookies中是否有登录信息
            if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
                #cookies中有登录信息　－　曾斤进记住密码
                #将cookies中的信息取出来再保存进session在返回到首页
                uid = request.COOKIES['uid']
                uphone = request.COOKIES['uphone']
                request.session['uid'] = uid
                request.session['uphone'] = uphone
                resp = redirect(url)
                return resp
            else:
                form = LoginForm()
                #将来访地址保存级cookies中(或者session)
                resp = render(request,'login.html',locals())
                resp.set_cookie('url',url)
                return resp

    else:
        #post请求，实现登录操作
        #获取手机号和密码
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        #判断手机号是否存在(登录是否成功)
        print(uphone,upwd)
        users = User.objects.filter(uphone=uphone,upwd=upwd)
        print(users)
        if users:
            #登录成功:先存进session
            request.session['uid']=users[0].id
            request.session['uphone'] = uphone
            #声明相应对象:从哪里来回哪里去
            url = request.COOKIES.get('url','/')
            resp = redirect(url)
            #将url从cookies中删除
            if 'url' in request.COOKIES:
                resp.delete_cookie('url')
            #判断是否要存进cookie
            if 'isSaved' in request.POST:
                expire = 60*60*24*90
                resp.set_cookie('uid',users[0].id,expire)
                resp.set_cookie('uphone',uphone,expire)
            return resp

        else:
            #登录失败
            form = LoginForm()
            return render(request,'login.html',locals())


def register_views(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        uphone = request.POST['uphone']
        upwd = request.POST['upwd']
        uname = request.POST['uname']
        uemail = request.POST['uemail']
        #先验证手机号在数据库中是否存在
        # users = User.objects.filter(uphone=uphone)
        # if users:
        #     #uphone已经存在
        #     errMsg = "手机号码已经存在"
        #     return render(request,'register.html',locals())
        #接受数据插入到数据库中
        user = User()
        user.uphone = uphone
        user.upwd = upwd
        user.uname = uname
        user.email = uemail
        user.save()
        #取出user中id 和　uphone的值保存进session
        request.session['uid']=user.id
        request.session['uphone']=user.uphone
        return redirect('/')

#检查手机号已经被注册过的函数
def check_uphone(request):
    #接受前段传递过来的数据
    uphone = request.GET['uphone']
    users = User.objects.filter(uphone=uphone)
    if users:
        status = 1
        msg = '手机号码已经存在'
    else:
        status = 0
        msg = "通过"
    dic = {
        'status':status,
        'msg':msg,
    }
    return HttpResponse(json.dumps(dic))

def index_views(request):
    return render(request,'new_project.html')

#检查session中是否有登录信息
#如果有则获取对应数据的uname值
def check_login_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        loginStatus = 1
        #通过uid的值获取对应uname
        id = request.session['uid']
        uname = User.objects.get(id=id).uname
        dic = {
            'loginStatus':loginStatus,
            'uname':uname
        }
        return HttpResponse(json.dumps(dic))
    else:
        dic = {
            'loginStatus':0
        }
        return HttpResponse(json.dumps(dic))

def logout_views(request):
    if 'uid' in request.session and 'uphone' in request.session:
        del request.session['uid']
        del request.session['uphone']
        #删除cookie值: resp.delete.cookie[]
        #构建响应对象
        url = request.META.get('HTTP_REFERER','/')
        resp = HttpResponseRedirect(url)
        #判断cookies中是否有登录信息，有的话，则删除
        if 'uid' in request.COOKIES and 'uphone' in request.COOKIES:
            resp.delete_cookie('uid')
            resp.delete_cookie('uphone')
        return resp
    return redirect('/')

#加载所有的商品类型，以及对应的每个类型下的前十条数据
def type_goods_views(request):
    all_list = []
    #加载所有的商品类型
    types = GoodsType.objects.all()
    for type in types:
        type_json = json.dumps(type.to_dict())
        #获取type类型下的最新的１０条数据
        g_list = type.goods_set.filter(isActive=True).order_by("-id")[0:10]
        #将g_list转换为json
        g_list_json = serializers.serialize('json',g_list)
        #将type_json和g_list_json封装到一个字典中
        dic = {
            "type":type_json,
            "goods":g_list_json,
        }
        #将dic字典追加到all_list中
        all_list.append(dic)
    return HttpResponse(json.dumps(all_list))

#将商品添加至购物车 或　更新现有商品的数量
def add_cart_views(request):
    #获取商品id,获取用户id,购买数量默认为1
    good_id = request.GET['gid']
    user_id = request.session['uid']
    ccount = 1
    #查看购物车中是否有相同用户购买的相同商品
    cart_list = CartInfo.objects.filter(user_id=user_id,goods_id=good_id)

    if cart_list:
        #购物车中已经有相同用户购买过相同商品,更新商品数量
        cartinfo = cart_list[0]
        cartinfo.ccount = cartinfo.ccount + ccount
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'更新数量成功'
        }
    else:
        #没有对应的用户以及对应的商品
        cartinfo = CartInfo()
        cartinfo.user_id = user_id
        cartinfo.goods_id = good_id
        cartinfo.ccount = ccount
        cartinfo.save()
        dic = {
            'status':1,
            'statusText':'添加购物车成功'
        }
    return HttpResponse(json.dumps(dic))

def cart_views(request):
    user_id = request.session['uid']
    user = User.objects.filter(user_id=user_id)
    return render(request,'cart.html',locals())




