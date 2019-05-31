from django.shortcuts import render
from django.http.response import JsonResponse, HttpResponseRedirect
import blog.tool as tool
import blog.models as models


def person_info(request):
    head = tool.getOnlineUser(request)
    return render(request, 'person_info.html',
                  {
                      'title': head['user_name'] + '的个人主页',
                      'head': head,
                      'user_name': head['user_name'],
                      'user_head': head['user_head'],
                      'introduce': head['introduce'],
                      'inPersonInfo': True
                  })


def person_complain(request):
    user_id = request.COOKIES.get('user_id')
    if user_id is None: return JsonResponse({'result': False})
    complains = models.complaint.objects.filter(user_id=user_id)
    data = {'list': tool.getComplaintData(complains)}
    return JsonResponse(data)


def person_collection(request):
    user_id = request.COOKIES.get('user_id')
    if user_id is None: return JsonResponse({'result': False})
    complains = models.collection_complaint.objects.filter(user_id=user_id)
    complaint_list = []
    for e in complains:
        complaint_list.append(e.collected_complaint_id)
    data = {'list': tool.getComplaintData(complaint_list)}
    return JsonResponse(data)


def person_reply(request):
    user_id = request.COOKIES.get('user_id')
    if user_id is None: return JsonResponse({'result': False})
    comment = models.comment.objects.filter(user_id=user_id)
    data = {'list': []}
    for e2 in comment:
        e = e2.complaint_id
        item = {
            'id': e.id,
            'title': e.title,
            'content': e.content,
            'user_name': e.user_id.username,
            'pic': tool.getPicPath(e.pic),  # 第一张图
            'reply_amount': e.reply_amount,
            'reply_content': e2.content
        }
        data['list'].append(item)
    return JsonResponse(data)


def person_edit(request):
    head = tool.getOnlineUser(request)
    return render(request, 'person_change.html', {
        'title': head['user_name'] + '的信息',
        'head': head,
        'user_name': head['user_name'],
        'user_head': head['user_head'],
        'email': head['email'] if head['email'] else '',
        'introduce': head['introduce'],
        'real_name': head['real_name'],
        'inPersonInfo': True
    })


def person_change(request):
    user_head = request.FILES.get("new_head", None)
    email = request.POST.get('email')
    real_name = request.POST.get('real_name')
    introduce = request.POST.get('introduce')
    name = tool.savePic(user_head)
    user_id = request.COOKIES.get('user_id')
    if user_id is None: return JsonResponse({'result': False})
    user = models.user.objects.get(id=user_id)

    user.email = email
    if name: user.user_head = name
    if user.introduce != introduce:
        user.introduce = introduce
    if user.real_name != real_name:
        user.real_name = real_name
    user.save()
    return HttpResponseRedirect('person_info')
