from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger


def company_post(request):
    return render(request, "company_post.html", {'isCompany': True})


def company_post_data(request):
    complaint_list = models.complaint.objects.filter(user_id__type=2)
    l = []
    for e in complaint_list:
        l.append({
            'id': e.id,
            'title': e.title,
            'content': e.content,
            'user_name': e.user_id.username,
            'pic': tool.getPicPath(e.pic),  # 第一张图
            'reply_amount': e.reply_amount,
            'head': tool.getHeadPath(e.user_id.user_head)
        })
    return JsonResponse({'list': l})
