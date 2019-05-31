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
    try:
        models.user.objects.get(username=user_name)
    except models.user.DoesNotExist:
        user = models.user(username=user_name, password=password, type=tool.GENERAL_USER)
        user.save()
        return HttpResponseRedirect('login_page')
    else:
        return JsonResponse({'result': False})


def logout(request):
    response = render(request, 'index.html', {
        'head': {
            'islogin': False,
        },
        'title': '主页'
    })
    response.delete_cookie('user_id')
    return response
