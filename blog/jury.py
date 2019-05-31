from django.shortcuts import render
from django.http.response import JsonResponse
import blog.models as models
import blog.tool as tool


def jury_page(request):
    jury_list = models.user.objects.filter(type=tool.JURY_USER)
    data = []
    for ju in jury_list:
        data.append({
            'jury_id': ju.id,
            'jury_name': ju.real_name,
            'jury_introduction': ju.introduce,
            'jury_head': tool.getHeadPath(ju.user_head),
        })

    return render(request, "jury.html", {
        'head': tool.getOnlineUser(request),
        'title': '评审团',
        'list': data,
        'isJury': True,
        'pic_ad': tool.getOnePicPath('1.jpg')
    })
