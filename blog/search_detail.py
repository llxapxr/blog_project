from django.db.models import Q
from django.shortcuts import render
from django.http.response import JsonResponse
import blog.tool as tool
import blog.models as models


def search_detail(request):
    key = request.GET.get('key')
    return render(request, 'search.html', {
        'key': key,
        'head': tool.getOnlineUser(request),
        'title': '搜索:' + key
    })


def search(request):
    key = request.GET.get('key')
    data = {'list': tool.getComplaintData(
        models.complaint.objects.filter(Q(title__contains=key) | Q(content__contains=key))
        )}
    return JsonResponse(data)
