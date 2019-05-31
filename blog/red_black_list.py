from django.shortcuts import render
from django.http.response import JsonResponse
import blog.tool as tool
import blog.models as models


def red_black_list(request):
    head = tool.getOnlineUser(request)

    red_rows = models.red_black.objects.filter(is_red=True).order_by('-score')
    black_rows = models.red_black.objects.filter(is_red=False).order_by('-score')
    red_list = []
    black_list = []
    num = 1
    for e in red_rows:
        red_list.append({
            'num': num,
            'company_name': e.company_id.company_name,
            'company_head': '../static/pic/' + e.company_id.company_head
        })
        num += 1
    num = 1
    for e in black_rows:
        black_list.append({
            'num': num,
            'company_name': e.company_id.company_name,
            'company_head': '../static/pic/' + e.company_id.company_head
        })
        num += 1

    return render(request, 'red_black.html', {
        'title': '企业信用评价表',
        'head': head,
        'red_list': red_list,
        'black_list': black_list,
        'isRedBlack': True
    })
