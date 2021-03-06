from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models


def login_page(request):
    return render(request, 'login_page.html', {
        'head': tool.getOnlineUser(request),
        'title': '登录'
    })


def register_page(request):
    return render(request, 'register_page.html', {
        'head': tool.getOnlineUser(request),
        'title': '注册'
    })


def login(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    try:
        user = models.user.objects.get(username=user_name)
    except models.user.DoesNotExist:
        return JsonResponse({'result': False})
    else:
        if password == user.password:
            response = HttpResponseRedirect('index')
            response.set_cookie('user_id', user.id, max_age=3600)  # 有效期一小时
            return response
        else:
            return JsonResponse({'result': False})


def register(request):
    user_name = request.GET.get('user_name')
    password = request.GET.get('password')
    type = request.GET.get('type')
    try:
        models.user.objects.get(username=user_name)
    except models.user.DoesNotExist:
        user = models.user(username=user_name, password=password, real_name='', type=type)
        user.save()
        return HttpResponseRedirect('login_page')
    else:
        return JsonResponse({'result': False})


def logout(request):
    pic1 = tool.getOnePicPath(tool.getStaticData('pic1'))
    pic2 = tool.getOnePicPath(tool.getStaticData('pic2'))
    pic3 = tool.getOnePicPath(tool.getStaticData('pic3'))
    pic1_title = tool.getStaticData('pic1_title')
    pic2_title = tool.getStaticData('pic2_title')
    pic3_title = tool.getStaticData('pic3_title')
    pic_ad = tool.getOnePicPath(tool.getStaticData('pic_ad'))
    response = render(request, 'index.html', {
        'head': {
            'islogin': False,
        },
        'title': '主页',
        'isIndex': True,
        'pic_ad': pic_ad,
        'pic1': pic1,
        'pic2': pic2,
        'pic3': pic3,
        'pic1_title': pic1_title,
        'pic2_title': pic2_title,
        'pic3_title': pic3_title
    })
    response.delete_cookie('user_id')
    return response
